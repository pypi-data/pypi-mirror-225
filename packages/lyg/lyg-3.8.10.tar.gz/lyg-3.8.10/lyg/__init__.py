import sys

version = sys.version_info[:2]

if version < (3, 9):
    raise ImportError("The lyg library supports only Python 3.9 and above. Please upgrade your Python version.")
else:
    suffix_map = {
        (3, 8): '38',
        (3, 9): '39',
        (3, 10): '310',
        (3, 11): '311',
    }

    try:
        version_suffix = suffix_map[version]
        module_name = f"tx.cp{version_suffix}-{'win_amd64' if sys.platform == 'win32' else 'x86_64-linux-gnu'}.pyd"
        tx = __import__(module_name)
    except KeyError:
        raise ImportError(f"The lyg library does not yet support Python {'.'.join(map(str, version))}.")

