import sys

version = sys.version_info[:2]

if version < (3, 8):
    raise ImportError("The lyg library supports only Python 3.8 and above. Please upgrade your Python version.")
elif version == (3, 8):
    from .python3_8 import tx
elif version == (3, 9):
    from .python3_9 import tx
elif version == (3, 10):
    from .python3_10 import tx
elif version == (3, 11):
    from .python3_11 import tx
else:
    raise ImportError(f"The lyg library does not yet support Python {'.'.join(map(str, version))}.")

