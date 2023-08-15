"""
Virtual FileSystem support.
"""

from uswarm.tools import parse_uri


# ----------------------------------------------------------
# Virtual File System
# ----------------------------------------------------------
class iVFS:  # noqa: R0903
    """Virtual File System interface"""

    def __init__(self, url: str):
        self.url = url

    def list(self):
        """a simple demo function"""

    def open(self):
        """a simple demo function"""

    def rename(self):
        """a simple demo function"""

    def delete(self):
        """a simple demo function"""


class FileSystem(iVFS):
    """Implementation of iVFS based on File System."""

    def __init__(self, url: str):
        super().__init__(url)
        self._uri = parse_uri(url)
        self.path = self._uri['path']
