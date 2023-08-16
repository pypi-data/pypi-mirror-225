
from abc import ABC, abstractmethod
from asyncio import AbstractEventLoop
from threading import RLock
import time
from typing import Dict, List, Optional
import uuid
from azure.core import MatchConditions
from azure.cosmos import CosmosClient, PartitionKey
from azure.cosmos import aio
from azure.cosmos.exceptions import (
    CosmosAccessConditionFailedError,
    CosmosResourceNotFoundError,
    CosmosResourceExistsError,
)
from .common import (
    CONTAINER_COMMIT, CONTAINER_META, DATABASE_DYNCONF, PARTITION_KEY_DATA,
    CommitRecord, DataItemRecord, MetaRecord,
)
from .utils import run_async_batch, Call



class ItemExisted(Exception):
    pass


##
## abstract
##

class DataAccessProxy(ABC):
    @abstractmethod
    def get_meta(self, app: str) -> Optional[MetaRecord]:
        ''' Get meta record by app.
            Args:
                app: dynamic config application name
            Returns:
                Got meta record, or None if not found.
        '''
        pass
    
    @abstractmethod
    def create_meta(self, meta: MetaRecord) -> MetaRecord:
        ''' Create meta record.
            Args:
                meta: meta record to create
            Returns:
                Created meta record.
            Raises:
                If meta record already exists, raise ItemExisted.
        '''
        pass
    
    @abstractmethod
    def update_meta_if_not_modified(self, meta: MetaRecord, etag: str) -> Optional[MetaRecord]:
        ''' Update meta record if given etag matched with remote _etag.
            Args:
                meta: meta record to update
                etag: etag to match
            Returns:
                Updated meta record, or None if etag conflicts.
            Raises:
                If meta record not exists, raise an exception.
        '''
        pass

    @abstractmethod
    def create_commit(self, commit: CommitRecord) -> CommitRecord:
        ''' Create commit record.
            Args:
                commit: commit record to create.
            Returns:
                Created commit record.
            Raises:
                If commit record already exists, raise ItemExisted.
        '''
        pass
    
    @abstractmethod
    def update_commit(self, commit: CommitRecord) -> CommitRecord:
        ''' Update commit record.
            Args:
                commit: commit record to update.
            Returns:
                Updated commit record.
            Raises:
                If commit record not exists, raise an exception.
        '''
        pass
    
    @abstractmethod
    def delete_commit(self, commit: CommitRecord) -> bool:
        ''' Delete commit record.
            Args:
                commit: commit record to delete.
            Returns:
                True: if commit existed and delete successfully.
                False: if commit not existed.
        '''
        pass
    
    @abstractmethod
    def query_commits_by_seq_range(self, app: str, seq_begin: int, seq_end: int) -> List[CommitRecord]:
        ''' Query commit records by sequence range.
            Args:
                app: dynamic config application name.
                seq_begin: begin of sequence range, inclusive.
                seq_end: end of sequence range, inclusive.
            Returns:
                List of queried commit records.
        '''
        pass
    
    @abstractmethod
    def query_data_items_by_commits(self, commit_ids: List[str]) -> List[DataItemRecord]:
        ''' Get all the data item records belonging to given commits.
            Args:
                commit_ids: commit ids to query
            Returns:
                Queried data item records.
        '''
        pass

    @abstractmethod
    def batch_upsert_data_items(self, data_items: List[DataItemRecord]):
        ''' Create or update for multiple data item records.
            No requirements for atomic/trasaction.
            Args:
                data_items: data item records to be upserted
        '''
        pass
    
    @abstractmethod
    def batch_delete_data_items(self, data_items: List[DataItemRecord]):
        ''' Delete multiple data item records. Ignore non-existed.
            No requirements for atomic/trasaction.
            Args:
                data_items: data item records to be deleted
        '''
        pass
    

##
## stubbed
##

class StubbedDataAccessProxy(DataAccessProxy):
    def __init__(self):
        self._metas: Dict[str, MetaRecord] = {}
        self._commits: Dict[str, CommitRecord] = {}
        self._data_items: Dict[str, DataItemRecord] = {}
        self._lock = RLock()


    def get_meta(self, app: str) -> Optional[MetaRecord]:
        meta = self._metas.get(app)
        if meta is None:
            return meta
        else:
            return meta.copy(deep=True)


    def create_meta(self, meta: MetaRecord) -> MetaRecord:
        new = meta.copy(deep=True)
        new.etag = str(uuid.uuid4())
        new.ts = int(time.time())
        with self._lock:
            if new.id in self._metas:
                raise ItemExisted('meta already exists')
            self._metas[new.id] = new
        return new.copy(deep=True)
            
    
    def update_meta_if_not_modified(self, meta: MetaRecord, etag: str) -> Optional[MetaRecord]:
        new = meta.copy(deep=True)
        new.etag = str(uuid.uuid4())
        new.ts = int(time.time())
        with self._lock:
            old = self._metas.get(meta.id)
            if old is None:
                raise Exception('meta not exists')
            if old.etag != etag:
                return None
            self._metas[new.id] = new
        return new.copy(deep=True)
            

    def create_commit(self, commit: CommitRecord) -> CommitRecord:
        new = commit.copy(deep=True)
        new.etag = str(uuid.uuid4())
        new.ts = int(time.time())
        with self._lock:
            if new.id in self._commits:
                raise ItemExisted('commit already exists')
            self._commits[new.id] = new
        return new.copy(deep=True)
    
    
    def update_commit(self, commit: CommitRecord) -> CommitRecord:
        new = commit.copy(deep=True)
        new.etag = str(uuid.uuid4())
        new.ts = int(time.time())
        with self._lock:
            if new.id not in self._commits:
                raise Exception('commit not exists')
            self._commits[new.id] = new
        return new.copy(deep=True)

    
    def delete_commit(self, commit: CommitRecord) -> bool:
        with self._lock:
            if commit.id in self._commits:
                self._commits.pop(commit.id)
                return True
            else:
                return False


    def query_commits_by_seq_range(self, app: str, seq_begin: int, seq_end: int) -> List[CommitRecord]:
        commits: List[CommitRecord] = []
        with self._lock:
            for commit in self._commits.values():
                if commit.app == app and seq_begin <= commit.seq <= seq_end:
                    commits.append(commit)
        return [c.copy(deep=True) for c in commits]
    
    
    def query_data_items_by_commits(self, commit_ids: List[str]) -> List[DataItemRecord]:
        commit_idset = set(commit_ids)
        ditems: List[DataItemRecord] = []
        with self._lock:
            for ditem in self._data_items.values():
                if ditem.commitId in commit_idset:
                    ditems.append(ditem)
        return [ditem.copy(deep=True) for ditem in ditems]
    
    
    def batch_upsert_data_items(self, data_items: List[DataItemRecord]):
        with self._lock:
            for ditem in data_items:
                new = ditem.copy(deep=True)
                new.etag = str(uuid.uuid4())
                new.ts = int(time.time())
                self._data_items[new.id] = new


    def batch_delete_data_items(self, data_items: List[DataItemRecord]):
        with self._lock:
            for ditem in data_items:
                if ditem.id in self._data_items:
                    self._data_items.pop(ditem.id)



##
## Cosmos Proxy
##

class CosmosDataAccessProxy(DataAccessProxy):
    ''' Designed for DynamicConfigConsumer.
        Cosmos synchronous client is not good at batch operations, some 
        batch functions are not implemented. Batch functions are only 
        required in DynamicConfigWriter.
    '''
    def __init__(self, client: CosmosClient, app: str, dbname: str = DATABASE_DYNCONF):
        assert app not in [CONTAINER_META, CONTAINER_COMMIT]
        self._app = app
        self._dbname = dbname
        self._client = client
        
        proxy_db = self._client.get_database_client(self._dbname)
        self._proxy_meta = proxy_db.get_container_client(CONTAINER_META)
        self._proxy_commit = proxy_db.get_container_client(CONTAINER_COMMIT)
        self._proxy_data = proxy_db.get_container_client(self._app)


    def get_meta(self, app: str) -> Optional[MetaRecord]:
        try:
            resp = self._proxy_meta.read_item(app, partition_key=app)
            return MetaRecord.parse_obj(resp)
        except CosmosResourceNotFoundError:
            return None
        
    
    def create_meta(self, meta: MetaRecord) -> MetaRecord:
        try:
            resp = self._proxy_meta.create_item(meta.dict())
            return MetaRecord.parse_obj(resp)
        except CosmosResourceExistsError as ex:
            raise ItemExisted('meta already exists') from ex
    

    def update_meta_if_not_modified(self, meta: MetaRecord, etag: str) -> Optional[MetaRecord]:
        try:
            resp = self._proxy_meta.replace_item(
                meta.id,
                meta.dict(),
                etag=etag,
                match_condition=MatchConditions.IfNotModified,
            )
            return MetaRecord.parse_obj(resp)
        except CosmosAccessConditionFailedError:
            return None


    def create_commit(self, commit: CommitRecord) -> CommitRecord:
        try:
            resp = self._proxy_commit.create_item(commit.dict())
            return CommitRecord.parse_obj(resp)
        except CosmosResourceExistsError as ex:
            raise ItemExisted('commit already exists') from ex
    

    def update_commit(self, commit: CommitRecord) -> CommitRecord:
        resp = self._proxy_commit.replace_item(commit.id, commit.dict())
        return CommitRecord.parse_obj(resp)
    

    def delete_commit(self, commit: CommitRecord) -> bool:
        try:
            self._proxy_commit.delete_item(commit.id, partition_key=commit.app)
            return True
        except CosmosResourceNotFoundError:
            return False
    

    def query_commits_by_seq_range(self, app: str, seq_begin: int, seq_end: int) -> List[CommitRecord]:
        cursor = self._proxy_commit.query_items(
            'SELECT * FROM c WHERE c.seq between @seqBegin and @seqEnd',
            parameters=[
                dict(name="@seqBegin", value=seq_begin),
                dict(name="@seqEnd", value=seq_end),
            ],
            partition_key=app,
        )
        return [CommitRecord.parse_obj(item) for item in cursor]
    

    def query_data_items_by_commits(self, commit_ids: List[str]) -> List[DataItemRecord]:
        cursor = self._proxy_data.query_items(
            'SELECT * FROM c WHERE ARRAY_CONTAINS(@L, c.commitId)',
            parameters=[
                dict(name='@L', value=commit_ids)
            ],
            enable_cross_partition_query=True,
        )
        return [DataItemRecord.parse_obj(item) for item in cursor]


    def batch_upsert_data_items(self, data_items: List[DataItemRecord]):
        raise NotImplementedError
    

    def batch_delete_data_items(self, data_items: List[DataItemRecord]):
        raise NotImplementedError
    
    
    
##
## Async Cosmos Proxy
##

class AsyncCosmosDataAccessProxy(DataAccessProxy):
    def __init__(
        self,
        client: aio.CosmosClient,
        loop: AbstractEventLoop,
        lock: RLock,
        app: str,
        dbname: str = DATABASE_DYNCONF,
    ):
        assert app not in [CONTAINER_META, CONTAINER_COMMIT]
        self._app = app
        self._dbname = dbname
        self._client = client
        self._loop = loop
        self._lock = lock
        
        proxy_db = self._client.get_database_client(self._dbname)
        self._proxy_meta = proxy_db.get_container_client(CONTAINER_META)
        self._proxy_commit = proxy_db.get_container_client(CONTAINER_COMMIT)
        self._proxy_data = self._get_or_create_app_container(proxy_db)
    
    
    def _get_or_create_app_container(self, proxy_db: aio.DatabaseProxy) -> aio.ContainerProxy:
        with self._lock:
            proxy_data = self._loop.run_until_complete(
                proxy_db.create_container_if_not_exists(self._app, PartitionKey(path=f"/{PARTITION_KEY_DATA}"))
            )
            return proxy_data
        

    def get_meta(self, app: str) -> Optional[MetaRecord]:
        with self._lock:
            try:
                resp = self._loop.run_until_complete(
                    self._proxy_meta.read_item(app, partition_key=app)
                )
                return MetaRecord.parse_obj(resp)
            except CosmosResourceNotFoundError:
                return None

    
    def create_meta(self, meta: MetaRecord) -> MetaRecord:
        with self._lock:
            try:
                resp = self._loop.run_until_complete(
                    self._proxy_meta.create_item(meta.dict())
                )
                return MetaRecord.parse_obj(resp)
            except CosmosResourceExistsError as ex:
                raise ItemExisted('meta already exists') from ex
            
    
    def update_meta_if_not_modified(self, meta: MetaRecord, etag: str) -> Optional[MetaRecord]:
        with self._lock:
            try:
                resp = self._loop.run_until_complete(
                    self._proxy_meta.replace_item(
                        meta.id,
                        meta.dict(),
                        etag=etag,
                        match_condition=MatchConditions.IfNotModified,
                    )
                )
                return MetaRecord.parse_obj(resp)
            except CosmosAccessConditionFailedError:
                return None
        

    def create_commit(self, commit: CommitRecord) -> CommitRecord:
        with self._lock:
            try:
                resp = self._loop.run_until_complete(
                    self._proxy_commit.create_item(commit.dict())
                )
                return CommitRecord.parse_obj(resp)
            except CosmosResourceExistsError as ex:
                raise ItemExisted('commit already exists') from ex
        
    
    def update_commit(self, commit: CommitRecord) -> CommitRecord:
        with self._lock:
            resp = self._loop.run_until_complete(
                self._proxy_commit.replace_item(commit.id, commit.dict())
            )
            return CommitRecord.parse_obj(resp)
        
    
    def delete_commit(self, commit: CommitRecord) -> bool:
        with self._lock:
            try:
                self._loop.run_until_complete(
                    self._proxy_commit.delete_item(commit.id, partition_key=commit.app)
                )
                return True
            except CosmosResourceNotFoundError:
                return False
        
    
    def query_commits_by_seq_range(self, app: str, seq_begin: int, seq_end: int) -> List[CommitRecord]:
        with self._lock:
            return self._loop.run_until_complete(
                self._query_commits_by_seq_range(app, seq_begin, seq_end)
            )
            

    async def _query_commits_by_seq_range(self, app: str, seq_begin: int, seq_end: int) -> List[CommitRecord]:
        cursor = self._proxy_commit.query_items(
            'SELECT * FROM c WHERE c.seq between @seqBegin and @seqEnd',
            parameters=[
                dict(name="@seqBegin", value=seq_begin),
                dict(name="@seqEnd", value=seq_end),
            ],
            partition_key=app,
        )
        commits: List[CommitRecord] = []
        async for item in cursor:
            commit = CommitRecord.parse_obj(item)
            commits.append(commit)
        return commits
        
    
    def query_data_items_by_commits(self, commit_ids: List[str]) -> List[DataItemRecord]:
        with self._lock:
            return self._loop.run_until_complete(
                self._query_data_items_by_commits(commit_ids)
            )


    async def _query_data_items_by_commits(self, commit_ids: List[str]) -> List[DataItemRecord]:
        cursor = self._proxy_data.query_items(
            'SELECT * FROM c WHERE ARRAY_CONTAINS(@L, c.commitId)',
            parameters=[
                dict(name='@L', value=commit_ids)
            ],
            partition_key=None,
        )
        drs: List[DataItemRecord] = []
        async for item in cursor:
            d = DataItemRecord.parse_obj(item)
            drs.append(d)
        return drs


    def batch_upsert_data_items(self, data_items: List[DataItemRecord]):
        with self._lock:
            self._loop.run_until_complete(
                self._batch_upsert_data_items(data_items)
            )
    
    
    async def _batch_upsert_data_items(self, data_items: List[DataItemRecord]):
        await run_async_batch(
            self._proxy_data.upsert_item,
            [Call(d.dict()) for d in data_items],
        )


    def batch_delete_data_items(self, data_items: List[DataItemRecord]):
        with self._lock:
            self._loop.run_until_complete(
                self._batch_delete_data_items(data_items)
            )
    
    
    async def _batch_delete_data_items(self, data_items: List[DataItemRecord]):
        async def delete_data_item(d: DataItemRecord):
            try:
                await self._proxy_data.delete_item(d.id, partition_key=d.key)
            except CosmosResourceNotFoundError:
                pass
        await run_async_batch(
            delete_data_item, 
            [Call(d) for d in data_items],
        )

