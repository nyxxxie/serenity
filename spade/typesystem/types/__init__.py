import pkgutil
from importlib import import_module

type_amt = 0 # This is used pretty much only in tests
__path__ = pkgutil.extend_path(__path__, __name__)
for _,modname,_ in pkgutil.walk_packages(path=__path__, prefix=__name__+"."):
    import_module(modname)
    type_amt = type_amt + 1
