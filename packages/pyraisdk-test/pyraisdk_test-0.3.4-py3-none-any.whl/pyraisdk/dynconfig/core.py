
from __future__ import annotations
from asyncio import AbstractEventLoop 
import json
from threading import RLock
import time
from typing import Any, Dict, List, Optional, Set
import uuid
from azure.cosmos import CosmosClient
from azure.cosmos import aio
from .proxy import (
    AsyncCosmosDataAccessProxy, 
    CosmosDataAccessProxy, 
    DataAccessProxy, 
    ItemExisted,
)
from .common import (
    MAX_COMMIT_CHAIN_LENGTH,
    MAX_COMMIT_DURATION_IN_SECONDS,
    MAX_WRITE_CONFLICT_RETRY_COUNT,
    CommitRecord,
    DataItemRecord, 
    MetaRecord,
)


class ExternalSequenceError(Exception):
    pass


class ChangeSet:
    def __init__(self):
        self._updates: Dict[str, Any] = {}
        self._deletions: Set[str] = set()

    def set(self, key: str, val: Any):
        self._updates[key] = val
        if key in self._deletions:
            self._deletions.remove(key)
            
    def delete(self, key: str):
        self._deletions.add(key)
        if key in self._updates:
            self._updates.pop(key)

    def is_empty(self) -> bool:
        return not self._updates and not self._deletions
    
    def __contains__(self, k: str):
        return k in self._updates or k in self._deletions
    
    def __eq__(self, other: Any) -> bool:
        if isinstance(other, ChangeSet):
            return self._updates == other._updates and self._deletions == other._deletions
        else:
            return False

    def apply_on(self, dataset: Dict[str, Any]):
        ''' Apply changeset on the input dataset.
        '''
        dataset.update(self._updates)
        for k in self._deletions:
            if k in dataset:
                dataset.pop(k)

    def update(self, sub: ChangeSet):
        for k, v in sub._updates.items():
            self.set(k, v)
        for k in sub._deletions:
            self.delete(k)

    @classmethod
    def compare(cls, src: Dict[str, Any], dst: Dict[str, Any]) -> ChangeSet:
        ''' Compare 2 datasets, and get the changeset from `src` to `dst`.
        '''
        changeset = ChangeSet()
        for key in src.keys() | dst.keys():
            if key in src:
                if key in dst:
                    src_val_str = json.dumps(src[key], sort_keys=True)
                    dst_val_str = json.dumps(dst[key], sort_keys=True)
                    if src_val_str != dst_val_str:
                        changeset.set(key, dst[key])
                else:
                    changeset.delete(key)
            else:
                if key in dst:
                    changeset.set(key, dst[key])
                else:
                    pass
        return changeset
    

class CommitChainManager:
    def __init__(self, proxy: DataAccessProxy, app: str):
        self._proxy = proxy
        self._app = app
        self._meta: MetaRecord = None
        self._commits: Dict[int, CommitRecord] = {}  # key: seq
    
    
    def get_meta(self) -> MetaRecord:
        if self._meta is None: 
            raise Exception('require refresh_chain first')
        return self._meta
    
    
    def get_sub_chain(self, seq_begin: int = None, seq_end: int = None) -> List[CommitRecord]:
        if seq_begin is None:
            seq_begin = self._meta.rootSeq
        if seq_end is None:
            seq_end = self._meta.topSeq
        return [self._commits[seq] for seq in range(seq_begin, seq_end + 1)]
        
        
    def get_top_commit(self) -> CommitRecord:
        return self._commits[self._meta.topSeq]
    
    
    def refresh_chain(self, enable_init: bool = True):
        ''' Update (or initialize) the commit chain to latest.
            Args:
                enable_init: Indicates whether to initialize meta record when it doesn't exist.
                             Will raise Exception when it's False and meta not found.
        '''
        # try to get latest meta
        # when meta not exist, try to create initial meta, if enable_init.
        meta = self._proxy.get_meta(self._app)
        if meta is None:
            if self._meta is not None:
                raise Exception(f'unexpected error to get meta record {self._app}')
            elif not enable_init:
                raise Exception(f'meta record {self._app} does not exist')
            else:
                # create meta
                try:
                    meta = self._proxy.create_meta(
                        MetaRecord(
                            id=self._app, 
                            topSeq=0,
                            rootSeq=1,
                            topCommitId='',
                            _etag='',
                            _ts=0,
                        )
                    )
                except ItemExisted:
                    # already exists, try get again
                    meta = self._proxy.get_meta(self._app)
                    if meta is None:
                        raise Exception(f'unexpected error for existed meta record {self._app}')
        
        # topSeq check for robustness, expect always meet.
        # But if somehow happend (can't imagine how), should raise out immediately.
        if self._meta is not None:
            assert self._meta.topSeq <= meta.topSeq

        # seq range of sub chain to fetch
        seq_begin = meta.rootSeq if self._meta is None else self._meta.topSeq + 1
        seq_end = meta.topSeq
        if seq_begin > seq_end:
            self._meta = meta
            return
        
        # query commit records and build chain
        commits = self._proxy.query_commits_by_seq_range(self._app, seq_begin, seq_end)
        chain = self.build_sub_commit_chain({c.id: c for c in commits}, seq_begin, seq_end, meta.topCommitId)
        if self._meta is not None:
            # validate the join point of the chain
            if chain[0].parentId != self._meta.topCommitId or chain[0].seq != self._meta.topSeq + 1:
                raise Exception(f'invalid commit {self._meta.topCommitId} at seq {self._meta.topSeq}')

        # update
        self._commits.update({c.seq: c for c in chain})
        self._meta = meta


    def create_commit(self, ext_seq: int) -> CommitRecord:
        commit_req = CommitRecord(
            id=str(uuid.uuid4()),
            app=self._app,
            seq=self._meta.topSeq + 1,
            parentId=self._meta.topCommitId,
            extSeq=ext_seq,
            _etag='',
            _ts=0,
        )
        commit_resp = self._proxy.create_commit(commit_req)
        return commit_resp


    def submit_commit(self, commit: CommitRecord, squash: bool = False) -> bool:
        ''' Try to submit commit.
            Returns:
                True: success
                False: indicates etag conflict
        '''
        # validate commit not submitted, for robustness
        # assume it was success, but we got an error caused by any reason
        sub_chain = self.get_sub_chain(seq_begin=commit.seq)
        if commit.id in (c.id for c in sub_chain):
            raise Exception(f'commit {commit.id} already submitted')

        # update commit
        if commit.seq != self._meta.topSeq + 1:
            commit.seq = self._meta.topSeq + 1
            commit.parentId = self._meta.topCommitId
            self._proxy.update_commit(commit)
        
        # update meta
        meta_req = self._meta.copy()
        meta_req.topSeq += 1
        meta_req.topCommitId = commit.id
        if squash:
            meta_req.rootSeq = meta_req.topSeq
        
        meta_resp = self._proxy.update_meta_if_not_modified(meta_req, meta_req.etag)
        return meta_resp is not None


    def fetch_changeset_of_chain(self, from_seq: int) -> ChangeSet:
        ''' Get the changeset from `from_seq` to `topSeq`.
            `from_seq` == 0 indicates it's in full mode.
        '''
        seq_begin = self._meta.rootSeq if from_seq == 0 else from_seq
        seq_end = self._meta.topSeq
        if seq_begin > seq_end:
            return ChangeSet()

        # chain & commits
        sub_chain: List[CommitRecord] = self.get_sub_chain(seq_begin, seq_end)
        id_commits: Dict[str, CommitRecord] = {c.id: c for c in sub_chain}
        
        # data query
        data_items = self._proxy.query_data_items_by_commits([c.id for c in sub_chain])

        # build changeset
        key_item: Dict[str, DataItemRecord] = {}
        key_seq: Dict[str, int] = {}
        for ditem in data_items:
            commit = id_commits.get(ditem.commitId)
            if commit is not None:
                if commit.seq > key_seq.get(ditem.key, 0):
                    key_item[ditem.key] = ditem
                    key_seq[ditem.key] = commit.seq
                    
        changeset = ChangeSet()
        for ditem in key_item.values():
            if ditem.deleted:
                changeset.delete(ditem.key)
            else:
                changeset.set(ditem.key, ditem.value)

        return changeset


    def put_changeset_into_commit(self, commit: CommitRecord, changeset: ChangeSet):
        if changeset.is_empty():
            return
        
        # build data records
        data_items: List[DataItemRecord] = []
        for k, v in changeset._updates.items():
            ditem = DataItemRecord(
                id=f'{k}:{commit.id}',
                commitId=commit.id,
                key=k,
                value=v,
                deleted=False,
                _etag='',
                _ts=0,
            )
            data_items.append(ditem)
        
        for k in changeset._deletions:
            ditem = DataItemRecord(
                id=f'{k}:{commit.id}',
                commitId=commit.id,
                key=k,
                value=None,
                deleted=True,
                _etag='',
                _ts=0,
            )
            data_items.append(ditem)
        
        # upsert items
        self._proxy.batch_upsert_data_items(data_items)


    def validate_ext_seq_inc(self, ext_seq: int):
        ''' Verify the incrementality of the external sequence
        '''
        if self._meta.topSeq == 0 or ext_seq < 0:
            return
        commit = self._commits[self._meta.topSeq]
        if ext_seq <= commit.extSeq:
            raise ExternalSequenceError(f'external seq violate incremental constraint: {commit.extSeq} to {ext_seq}') 


    @staticmethod
    def build_sub_commit_chain(
        commits: Dict[str, CommitRecord], seq_begin: int, seq_end: int, end_commit_id: str
    ) -> List[CommitRecord]:
        ''' Build commit chain.
        '''
        chain = []
        commit_id = end_commit_id
        for seq in range(seq_end, seq_begin - 1, -1):
            commit = commits.get(commit_id)
            if commit is None or commit.seq != seq:
                raise Exception(f'invalid commit {commit_id} at seq {seq}')
            chain.append(commit)
            commit_id = commit.parentId
        chain.reverse()
        return chain


class DynamicConfigWriter:
    ''' Dynamic Config Writer.
    '''
    
    def __init__(
        self,
        proxy: DataAccessProxy,
        app: str,
    ):
        self._chainman = CommitChainManager(proxy, app)
        self._lock = RLock()
    
    
    @classmethod
    def from_cosmos_client(
        cls, client: aio.CosmosClient, app: str, loop: AbstractEventLoop, lock: RLock
    ) -> DynamicConfigWriter:
        ''' Create dynamic config writer with cosmos async client.
        
            Args:
                client: cosmos async client
                app: application name
                loop: event loop bind with cosmos async client
                lock: mutex for event loop
                
            Returns:
                dynamic config writer
        '''
        proxy = AsyncCosmosDataAccessProxy(client, loop, lock, app)
        return DynamicConfigWriter(proxy, app)


    def reconcile(self, dataset: Dict[str, Any], ext_seq: int = -1) -> ChangeSet:
        ''' Make remote dataset consistent with input `dataset`. 
            Success of reconcile guarantee at that moment remote dataset
            is completely same with local input `dataset`.
            
            Args:
                dataset: Local full dataset to sync to remote.
                ext_seq: An extra external sequence. For non-negative values, require
                        them to be incremental in commit chain.
            
            Returns:
                The changeset updated to remote in new commit.
        '''
        with self._lock:
            return self._reconcile(dataset, ext_seq)
    
    
    def gc(self):
        ''' Garbage collect.
            Can be executed at any time. Include 2 steps:
            1. sqaush commit chain
            2. collect commit garbage
        '''
        with self._lock:
            self._squash_commit_chain()
            self._collect_commit_garbage()
    
    
    def _reconcile(self, dataset: Dict[str, Any], ext_seq: int = -1) -> ChangeSet:
        next_pull_seq = 0
        remote_dataset = {}
        commit_changeset = ChangeSet()
        commit: CommitRecord = None
        ts_start = time.time()
        
        for trial in range(MAX_WRITE_CONFLICT_RETRY_COUNT):
            self._chainman.refresh_chain()

            # has more remote data
            if next_pull_seq <= self._chainman.get_meta().topSeq:
                # get data
                pulled = self._chainman.fetch_changeset_of_chain(next_pull_seq)
                next_pull_seq = self._chainman.get_meta().topSeq + 1
                pulled.apply_on(remote_dataset)

                # get delta
                if trial == 0:
                    # full delta, for first time
                    delta = ChangeSet.compare(remote_dataset, dataset)
                    if delta.is_empty():
                        # nothing to commit, success automatically
                        return commit_changeset
                else:
                    # incremental delta (save cost of value compare):
                    # 1. only in scope of keys in `pulled`
                    # 2. exclude Keys already in `commit_changeset`
                    delta = ChangeSet.compare(
                        {k: v for k, v in remote_dataset.items() if k in pulled and k not in commit_changeset}, 
                        {k: v for k, v in dataset.items()        if k in pulled and k not in commit_changeset}, 
                    )

                # check ext seq
                self._chainman.validate_ext_seq_inc(ext_seq)
                
                # write delta
                if commit is None:
                    commit = self._chainman.create_commit(ext_seq)
                self._chainman.put_changeset_into_commit(commit, delta)
                commit_changeset.update(delta)
            
            # max duration check
            if time.time() - ts_start > MAX_COMMIT_DURATION_IN_SECONDS:
                raise Exception(f'timeout for commit duration')
            
            # try submit
            success = self._chainman.submit_commit(commit)
            if success:
                return commit_changeset
                
        raise Exception('exceed max write conflict retries')

    
    def _squash_commit_chain(
        self, 
        max_commit_chain_length: int = MAX_COMMIT_CHAIN_LENGTH,
    ):
        ''' To avoid the commit chain being too long, need to quash the long chain.
            Read out the full dataset from remote, and submit the dataset in one
            commit to overwrite the old data.
        '''
        # check chain length
        self._chainman.refresh_chain(enable_init=False)
        chain_len = self._chainman.get_meta().topSeq - self._chainman.get_meta().rootSeq + 1
        if chain_len <=  max_commit_chain_length:
            return
        
        # init
        ts_start = time.time()
        ext_seq = self._chainman.get_top_commit().extSeq
        commit = self._chainman.create_commit(ext_seq)
        next_pull_seq = 0
        
        for trial in range(MAX_WRITE_CONFLICT_RETRY_COUNT):
            self._chainman.refresh_chain(enable_init=False)
            commit.extSeq = self._chainman.get_top_commit().extSeq
            
            # has more remote data
            if next_pull_seq <= self._chainman.get_meta().topSeq:
                # get data
                pulled = self._chainman.fetch_changeset_of_chain(next_pull_seq)
                next_pull_seq = self._chainman.get_meta().topSeq + 1
            
                # remove deletions for first pull (full dataset)
                if trial == 0:
                    pulled._deletions.clear()
                
                # write data
                self._chainman.put_changeset_into_commit(commit, pulled)
                
            # max duration check
            if time.time() - ts_start > MAX_COMMIT_DURATION_IN_SECONDS:
                raise Exception(f'timeout for commit duration')
            
            # try submit
            success = self._chainman.submit_commit(commit, squash=True)
            if success:
                return
        
        # failed exceed max retry
        raise Exception('exceed max write conflict retries')
    

    def _collect_commit_garbage(
        self,
        garbage_retenion_duration: float = MAX_COMMIT_DURATION_IN_SECONDS * 2,
    ):
        ''' Failed commits produce garbage. Need regular cleaning.
            Since can't distinguish gargabe and onging commits easily, only
            clear commits meeting all following conditions:
            1. Not in chain
            2. seq <= topSeq
            3. Inactive for long enough (12 hours)
        '''
        self._chainman.refresh_chain(enable_init=False)
        meta = self._chainman.get_meta()
        
        # build full commit chain
        commits_all = self._chainman._proxy.query_commits_by_seq_range(
            self._chainman._app, 1, meta.topSeq)
        
        chain = self._chainman.build_sub_commit_chain(
            {c.id: c for c in commits_all}, 1, meta.topSeq, meta.topCommitId)
        
        commits_in_chain = {c.id: c for c in chain}
        
        # scan
        now = time.time()
        for commit in commits_all:
            # in chain
            if commit.id in commits_in_chain:
                continue
            # seq out of scope
            if commit.seq > meta.topSeq:
                continue
            # inactive not long enough
            if commit.ts > now - garbage_retenion_duration:
                continue
            # delete garbage commit & data
            data_items = self._chainman._proxy.query_data_items_by_commits([commit.id])
            self._chainman._proxy.batch_delete_data_items(data_items)
            self._chainman._proxy.delete_commit(commit)



class DynamicConfigConsumer:
    ''' Dynamic Config Consumer.
    '''
    def __init__(
        self,
        proxy: DataAccessProxy,
        app: str,
    ):
        self._chainman = CommitChainManager(proxy, app)
        self._lock = RLock()
        self._next_pull_seq = 0
        
    
    @classmethod
    def from_cosmos_client(cls, client: CosmosClient, app: str) -> DynamicConfigConsumer:
        ''' Create dynamic config consumer with cosmos client.
        
            Args:
                client: cosmos client
                app: application name
                
            Returns:
                dynamic config consumer
        '''
        proxy = CosmosDataAccessProxy(client, app)
        return DynamicConfigConsumer(proxy, app)


    def pull(self) -> Optional[ChangeSet]:
        ''' Pull changesets incrementally.
            First time will get the full dataset.
            Returns:
                None if no newer commits; or will get the changeset.
        '''
        with self._lock:
            self._chainman.refresh_chain(enable_init=False)
            if self._next_pull_seq <= self._chainman.get_meta().topSeq:
                pulled = self._chainman.fetch_changeset_of_chain(self._next_pull_seq)
                self._next_pull_seq = self._chainman.get_meta().topSeq + 1
                return pulled
            else:
                return None
    
    
    def reset(self):
        ''' Reset the "_next_pull_seq".
            Will pull full dataset for next time.
        '''
        with self._lock:
            self._next_pull_seq = 0

