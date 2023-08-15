"""Main module."""
from datetime import datetime
from typing import Union, List, Dict, Tuple, Any


from .filesystem import iVFS


# ----------------------------------------------------------
# Record
# ----------------------------------------------------------
class Record(dict):
    """Base Class for any record that may be stored in an
    Incremental Storage.


    """

    ORDER: List = []

    @classmethod
    def set_order(cls, order: Union[List, Dict, Tuple]) -> None:
        """Set the render order for all record of the same class."""
        cls.ORDER = ["key", "time"] + list(order)

    def __init__(self, *args, **kw):
        self["time"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")
        super().__init__(*args, **kw)

    def items(self):
        keys = list(self.keys())
        for key in self.ORDER:
            if key in self:
                yield key, self[key]
                keys.remove(key)

        for key in keys:
            yield key, self[key]


# ----------------------------------------------------------
# Storage
# ----------------------------------------------------------
class Storage:
    """Interface for Incremental Storage"""

    def __init__(self, fs: iVFS):
        assert isinstance(fs, iVFS)
        self.fs = fs


# ----------------------------------------------------------
# Cluster
# ----------------------------------------------------------


class iCluster:
    """Data Partition of Storage.
    Handles writing records to iVFS.
    """

    def __init__(self, storage: Storage, lbound: Any, rbound: Any):
        self.storage = storage
        self.lbound = lbound
        self.rbound = rbound
        self.pointer = self.storage.fs.open()

    def add(self, record: Record):
        """Add record to cluster"""
        payload = record.items()
