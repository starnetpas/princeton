# check_distutils.py
try:
    from distutils.version import LooseVersion
    print("distutils is installed and working!")
except ImportError as e:
    print("distutils not found:", e)

