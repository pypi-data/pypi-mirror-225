import sys

if sys.version_info < (3, 9):
    raise ImportError("The lyg library supports only Python 3.9 and above. Please upgrade your Python version.")

if sys.platform == "win32":
    platform_suffix = f"cp{sys.version_info.major}{sys.version_info.minor}-win_amd64.pyd"
else:
    platform_suffix = f"cpython-{sys.version_info.major}{sys.version_info.minor}-x86_64-linux-gnu.so"

from . import platform_suffix as tx

