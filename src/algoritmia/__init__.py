import sys

TVERSION = (4, 0, 1)  # Recuerda cambiarlo también en 'pyproject.toml' <--------- !!!!!
VERSION = '.'.join([str(e) for e in TVERSION])

python_version = sys.version_info

if python_version[0:2] < (3, 12):
    raise ImportError(f"Library 'algoritmia' ({VERSION}) requires Python 3.12 or higher")

