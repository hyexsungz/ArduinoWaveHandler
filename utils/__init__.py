import importlib
import pkgutil

__all__ = []

_modules = [
    "console",
    "file_utils",
    "logger",
    "parser",
    "string_utils",
    "time_utils"
]

for module_name in _modules:
    try:
        module = importlib.import_module(f".{module_name}", package=__name__)
        globals()[module_name] = module
        __all__.append(module_name)
    except Exception as e:
        globals()[module_name] = None

def reload_all():
    for module_name in _modules:
        try:
            importlib.reload(globals().get(module_name))
        except Exception:
            pass

def list_modules():
    return [m for m in _modules if globals().get(m) is not None]

def get_status():
    return {
        "loaded": list_modules(),
        "total": len(_modules)
    }