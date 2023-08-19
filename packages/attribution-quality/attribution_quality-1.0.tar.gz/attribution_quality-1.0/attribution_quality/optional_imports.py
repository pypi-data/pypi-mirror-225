"""This class allows for the use of SimpleITK for typing and checks at runtime even if it is not installed"""
import warnings


class DummyModule:
    def __init__(self, module_name):
        self.__module_name = module_name
        self.is_dummy = True
        warnings.filterwarnings('always', '.*(may prevent some methods).*')
        warnings.warn(f'ImportWarning: {self.__module_name} cannot be imported. This may prevent some methods from working as intended', RuntimeWarning, stacklevel=2)

    def imread(self, *args, **kwargs):
        warnings.warn(f'RuntimeWarning: called method requires {self.__module_name} to be installed', RuntimeWarning, stacklevel=2)

    def __getattr__(self, attr):
        # This allows `SimpleITK.Image` to be used for typing without raising an error (and similar cases), but all attributes return as None
        # NOTE: hasattr() only checks if __getattr__ throws an `AttributeError`, so it will always be true for this class
        warnings.warn(f'RuntimeWarning: called method requires {self.__module_name} to be installed', RuntimeWarning, stacklevel=2)


try:
    import SimpleITK
except ImportError:
    SimpleITK = DummyModule('SimpleITK')
except ModuleNotFoundError:
    SimpleITK = DummyModule('SimpleITK')
