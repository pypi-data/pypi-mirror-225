import time

from typing import Literal

from collections import defaultdict
import struct
import abc


AggID = Literal['SUM', 'MEAN', 'MIN', 'MAX']


def bytes2double(value: bytes) -> float:
    return struct.unpack("d", value)[0]


def double2bytes(agg_value: float) -> bytes:
    return struct.pack("d", agg_value)


class CollectionNameError(Exception):
    pass


class UnsupportedAgg(Exception):
    pass


class TooManyAttempts(Exception):
    pass


class StateABC(abc.ABC):
    @abc.abstractmethod
    def connect_collection(self, collection: str, ttl: int = 0, aggregator_id: AggID = None) -> None:
        pass

    @abc.abstractmethod
    def get_keys(self, collection: str) -> list[str] | None:
        pass

    @abc.abstractmethod
    def get_value(self, collection: str, key: str) -> bytes | None:
        pass

    @abc.abstractmethod
    def del_value(self, collection: str, key: str) -> None:
        pass

    @abc.abstractmethod
    def set_value(self, collection: str, key: str, value: bytes) -> bytes | None:
        pass

    @abc.abstractmethod
    def get_agg(self, collection: str, key: str) -> float | None:
        pass

    @abc.abstractmethod
    def upd_agg(self, collection: str, key: str, cur_sample: float = 1.0) -> None:
        pass


class InmemKV(StateABC):
    def __init__(self):
        self.collections = defaultdict(lambda: defaultdict(lambda: None))
        self.ttls = defaultdict(int)
        self.aggregator_ids = defaultdict(lambda: None)
        self.revisions = defaultdict(lambda: defaultdict(int))

    def connect_collection(self, collection: str, ttl: int = 0, aggregator_id: AggID = None):
        if ttl:
            self.ttls[collection] = ttl
        if aggregator_id:
            self.aggregator_ids[collection] = aggregator_id

    def get_keys(self, collection: str) -> list[str] | None:
        return list(self.collections[collection].keys())

    def _delete_old_values(self, collection):
        ttl = self.ttls[collection]
        if not ttl:
            return
        cur_time = time.time()
        cur_collection = self.collections[collection]
        self.collections[collection] = defaultdict(lambda: None, {
            key: rec for key, rec in cur_collection.items()
            if rec and (cur_time - rec[0]) <= ttl
        })

    def get_value(self, collection: str, key: str) -> bytes | None:
        rec = self.collections[collection][key]
        if not rec:
            return None
        return rec[1]  # value, ts = rec

    def del_value(self, collection: str, key: str) -> None:
        self.collections[collection].pop(key, 0)

    def set_value(self, collection: str, key: str, value: bytes) -> bytes | None:
        self.collections[collection][key] = (time.time(), value)
        self._delete_old_values(collection)

    def get_agg(self, collection: str, key: str) -> float | None:
        value = self.get_value(collection, key)
        return bytes2double(value) if value is not None else None

    def upd_agg(self, collection: str, key: str, cur_sample: float = 1.0) -> None:
        aggregator_id = self.aggregator_ids[collection]
        last_agg = self.get_agg(collection, key)
        if aggregator_id == 'MEAN':
            self.revisions[collection][key] += 1
        if last_agg is None:
            new_agg = cur_sample
        elif aggregator_id == 'SUM':
            new_agg = last_agg + cur_sample
        elif aggregator_id == 'MEAN':
            n = self.revisions[collection][key]
            new_agg = (last_agg * (n - 1) + cur_sample) / n
        elif aggregator_id == 'MIN':
            new_agg = last_agg if last_agg < cur_sample else cur_sample
        elif aggregator_id == 'MAX':
            new_agg = last_agg if last_agg > cur_sample else cur_sample
        else:
            raise UnsupportedAgg(f'UnsupportedAgg {aggregator_id}')
        self.set_value(collection, key, double2bytes(new_agg))
