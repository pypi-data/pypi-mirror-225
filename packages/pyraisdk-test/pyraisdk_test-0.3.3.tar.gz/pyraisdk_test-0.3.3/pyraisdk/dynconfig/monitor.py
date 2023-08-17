
from __future__ import annotations
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
import heapq
from threading import Condition, RLock, Thread
import time
import traceback
from typing import Any, Dict, List, Optional, Set, Tuple, Union
from azure.core.credentials import TokenCredential
from azure.cosmos import CosmosClient
from pyraisdk import rlog
from .core import ChangeSet, DynamicConfigConsumer
from .proxy import CosmosDataAccessProxy, DataAccessProxy


class ConfigMonitor(ABC):
    ''' Base class for Dynamic Config Monitors to inherit from.
    '''
    def __init__(
        self,
        url: str,
        credential: Union[str, Dict[str, str], TokenCredential],
        app: str,
        interval: float = 10,
    ):
        ''' Constructor. Won't really run until 'start' called.
            Args:
                url: The URL of the Cosmos DB account.
                credential: Can be the account key, or a dictionary of resource tokens.
                app: Application name of dynamic config.
                interval: Check interval in seconds. Default 10.
        '''
        self.__url = url
        self.__credential = credential
        self.__app = app
        self.__interval = interval
        # init load status
        self.__init_load_done: bool = False
        self.__init_load_cond = Condition()
        self.__init_load_excepted: Optional[Exception] = None
    

    def _set_init_load_status(self, success: bool, excepted: Optional[Exception]):
        if self.__init_load_done:
            return
        with self.__init_load_cond:
            if success:
                self.__init_load_done = True
                self.__init_load_excepted = None
                self.__init_load_cond.notify_all()
            else:
                assert excepted is not None
                self.__init_load_excepted = excepted
                self.__init_load_cond.notify_all()


    def wait_init_load(self, timeout: Optional[float] = None):
        ''' Wait for initial loading '''
        with self.__init_load_cond:
            if self.__init_load_done:
                return
            elif self.__init_load_excepted is not None:
                raise self.__init_load_excepted
        
            notified = self.__init_load_cond.wait(timeout)
            if notified:
                if self.__init_load_done:
                    return
                elif self.__init_load_excepted is not None:
                    raise self.__init_load_excepted
                else:
                    raise Exception('unexpected error')
            else:
                raise TimeoutError('initial loading timeout')


    def start(self, blocking: bool = False, timeout: Optional[float] = None):
        ''' Start config monitor
            Args:
                blocking: If True, block until initial loading complete for fail;
                    If False, return immediately.
                timeout: When blocking is True and it blocks exceed 'timeout', will
                    raise the TimeoutError exception. None for no timeout limitation.
        '''
        _manager.start_config_monitor(
            self, self.__url, self.__credential, self.__app, self.__interval
        )
        if blocking:
            self.wait_init_load(timeout)
        

    def close(self):
        ''' Stop config monitor '''
        _manager.stop_config_monitor(self)


    @abstractmethod
    def apply(self, updates: Dict[str, Any], deletions: Set[str]):
        ''' Monitor apply function.
        
            Abstract method which need to be implemented in subclass. It receives
            a changeset (include updates and deletions) of one/multiple commits.
            
            Args:
                updates: key-value to be updated
                deletions: keys to be deleted
        '''
        pass



@dataclass
class _MonitorHandler:
    app: str
    monitor: ConfigMonitor
    consumer: DynamicConfigConsumer
    interval: float
    next_ts: float = 0
    lock: RLock = field(default_factory=RLock)
    unapplied: Optional[ChangeSet] = None


class _MonitorManager:
    def __init__(self):
        self._handlers: Dict[int, _MonitorHandler] = {}
        self._priority: List[Tuple[float, _MonitorHandler]] = []
        self._clients: Dict[str, CosmosClient] = {}
        self._cond = Condition()
        self._pool = ThreadPoolExecutor()
        self._worker: Optional[Thread] = None
        
    
    def start_config_monitor(
        self,
        monitor: ConfigMonitor,
        url: str,
        credential: Union[str, Dict[str, str], TokenCredential],
        app: str,
        interval: float,
    ):
        # get cosmos client
        with self._cond:
            if url in self._clients:
                client = self._clients[url]
            else:
                client = CosmosClient(url, credential)
                self._clients[url] = client
        
        # start
        proxy = CosmosDataAccessProxy(client, app)
        self._start_config_monitor_with_access_proxy(monitor, proxy, app, interval)


    def _start_config_monitor_with_access_proxy(
        self,
        monitor: ConfigMonitor,
        proxy: DataAccessProxy,
        app: str,
        interval: float,
    ):
        with self._cond:
            # set handler
            consumer = DynamicConfigConsumer(proxy, app)
            handler = _MonitorHandler(app, monitor, consumer, interval)
            monitor_id = id(monitor)
            if monitor_id in self._handlers:
                raise Exception(f'ConfigMonitor {monitor_id} already started')
            else:
                heapq.heappush(self._priority, (handler.next_ts, handler))
                self._handlers[monitor_id] = handler

            # init worker
            if self._worker is None:
                self._worker = Thread(target=self._worker_run, daemon=True)
                self._worker.start()
            else:
                self._cond.notify_all()


    def stop_config_monitor(self, monitor: ConfigMonitor):
        with self._cond:
            monitor_id = id(monitor)
            if monitor_id in self._handlers:
                self._handlers.pop(monitor_id)


    def _worker_run(self):
        while True:
            try:
                self._worker_run_inner()
            except Exception as ex:
                if rlog._logger_initialized:
                    rlog.errorcf('', -1, ex, f'{EVENT_KEY_PREFIX}: unexpected error in manager worker')
                else:
                    traceback.print_exc()
                time.sleep(3)


    def _worker_run_inner(self):
        with self._cond:
            while True:
                if len(self._priority) == 0:
                    self._cond.wait()
                else:
                    _, handler = heapq.heappop(self._priority)
                    monitor_id = id(handler.monitor)
                    notified = self._cond.wait(handler.next_ts - time.time())
                    
                    # new handler added
                    if notified:
                        heapq.heappush(self._priority, (handler.next_ts, handler))
                        continue
                    
                    # current handler deleted
                    if monitor_id not in self._handlers:
                        continue
                    
                    # next ts
                    handler.next_ts = time.time() + handler.interval
                    heapq.heappush(self._priority, (handler.next_ts, handler))
                    
                    # pull & apply
                    try:
                        has_more = self._has_more_for_consumer(handler.consumer)
                    except Exception as ex:
                        self._handle_monitor_exception(handler, ex)
                        continue
                    if has_more:
                        self._pool.submit(self._pull_and_apply, handler)


    def _has_more_for_consumer(self, consumer: DynamicConfigConsumer) -> bool:
        acquired = consumer._lock.acquire(blocking=False)
        if not acquired:
            return False
        try:
            consumer._chainman.refresh_chain(enable_init=False)
            return consumer._next_pull_seq <= consumer._chainman.get_meta().topSeq
        finally:
            consumer._lock.release()


    def _pull_and_apply(self, handler: _MonitorHandler):
        acquired = handler.lock.acquire(blocking=False)
        if not acquired:
            return
        try:
            # pull
            pulled = handler.consumer.pull()
            if pulled is None:
                return
            
            if handler.unapplied is None:
                handler.unapplied = pulled
            else:
                handler.unapplied.update(pulled)
                
            # apply
            handler.monitor.apply(handler.unapplied._updates, handler.unapplied._deletions)
            handler.unapplied = None
            
            # init load success
            handler.monitor._set_init_load_status(True, None)
            
        except Exception as ex:
            self._handle_monitor_exception(handler, ex)
            
        finally:
            handler.lock.release()


    def _handle_monitor_exception(self, handler: _MonitorHandler, excepted: Exception):
            # init load status
            handler.monitor._set_init_load_status(False, excepted)
            # logging
            if rlog._logger_initialized:
                rlog.event(f'{EVENT_KEY_PREFIX}_MonitorProcessError', handler.app, 0)
                rlog.errorcf('', -1, excepted, f'{EVENT_KEY_PREFIX}: monitor process error, app: {handler.app}')
            else:
                traceback.print_exception(type(excepted), excepted, excepted.__traceback__)



# logging key prefix for monitor
EVENT_KEY_PREFIX = 'pyraidynconf'

# singleton
_manager = _MonitorManager()

