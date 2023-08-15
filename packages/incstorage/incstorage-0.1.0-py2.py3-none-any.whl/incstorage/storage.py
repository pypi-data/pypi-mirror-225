"""
TODO: Incremental Storage Module
"""


# ----------------------------------------------------------
# Virtual File System
# ----------------------------------------------------------
class iVFS:  # noqa: R0903
    """Virtual File System interface"""

    def __init__(self, url: str):
        pass

    def afoo(self):
        """a simple demo function"""

    def abar(self):
        """a simple demo function"""


class FileSystem(iVFS):
    """Implementation of iVFS based on File System."""

    def __init__(self, url: str):
        pass


# ----------------------------------------------------------
# Storage
# ----------------------------------------------------------
class iStorage:
    """Interface for Incremental Storage"""

    def __init__(self, fs: iVFS):
        self.fs = fs

    def afoo(self):
        """a simple demo function"""

    def abar(self):
        """a simple demo function"""


class Storage(iStorage):
    """Storage Implementation."""

    def __init__(self, url: str):
        super().__init__(url)
