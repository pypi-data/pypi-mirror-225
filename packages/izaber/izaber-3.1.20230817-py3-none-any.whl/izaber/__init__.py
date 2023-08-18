import sys
import re
import importlib

try:
    from importlib.metadata import version
    __version__ = version("izaber")
# For older versions of python
except:
    import pkg_resources
    __version__ = pkg_resources.get_distribution("izaber").version

# Check to see the library has the submodule we need
class IZaberLoaderImportlib(object):

    def __init__(self,spec,module_name,*args,**kwargs):
        self.spec = spec
        self.module_name = module_name
        self.args = args
        self.kwargs = kwargs

    def load_module(self, module_name):
        # In the case of pyinstaller, it seems to set sys.frozen
        # we check for that and load the module directly
        if hasattr(sys,'frozen'):
            module = self.spec.loader.load_module(self.spec.name)
            sys.modules[self.module_name] = module
            sys.modules[module_name] = module
            sys.modules[self.spec.name] = module
            self.spec.loader.exec_module(module)
        else:
            if self.spec.name in sys.modules:
                module = sys.modules[self.spec.name]
                sys.modules.setdefault(self.module_name, module)
                sys.modules.setdefault(module_name, module)
            else:
                module = importlib.util.module_from_spec(self.spec)
                sys.modules[self.module_name] = module
                sys.modules[module_name] = module
                sys.modules[self.spec.name] = module
                self.spec.loader.exec_module(module)
        return module

class IZaberSpec:
    def __init__(self, spec, module_name):
        self.spec = spec
        self.module_name = module_name
        self.loader = IZaberLoaderImportlib(spec, module_name)

    def __getattr__(self, k):
        return getattr(self.spec, k)

from importlib import abc as il_abc
class IZaberFinderImportlib(il_abc.MetaPathFinder):
    """ Attempts to finds the module that may be tucked into
        a submodule.
    """

    def __init__(self,prefixes=None):
        super(IZaberFinderImportlib,self).__init__()
        if prefixes is None:
            prefixes = ['izaber.']
        self.prefixes = prefixes

    def add_prefix(self,prefix):
        normalized_prefix = prefix+'.'
        if normalized_prefix not in self.prefixes:
            self.prefixes.append(normalized_prefix)
            self.prefixes.sort(key=lambda a:len(a),reverse=True)

    def attempt_load(self,prefix,module_name):
        # Extension modules are expected to be named:
        #
        # izaber_extensionname
        #
        # where extensionname is all alphabetical 
        try:
            target_module = re.sub(
                          '^'+prefix,
                          prefix.replace('.','_'),
                          module_name,
                      )

            found = None
            spec = None
            package_path = []
            for e in target_module.split('.'):
                package = "_".join(package_path) or None
                spec = importlib.util.find_spec(e,package)
                if not spec:
                    raise ModuleNotFoundError(f"No module named {module_name}")
                package_path.append(e)

            return IZaberLoaderImportlib(spec,module_name)
        except ImportError:
            return

    def find_spec(self, module_name, path=None, target=None):

        for prefix in self.prefixes:
            try:
                if module_name.index(prefix) != 0:
                    continue
            except ValueError:
                continue

            try:
                target_module = re.sub(
                              '^'+prefix,
                              prefix.replace('.','_'),
                              module_name,
                          )

                found = None
                spec = None
                package_path = []
                for e in target_module.split('.'):
                    package = "_".join(package_path) or None
                    spec = importlib.util.find_spec(e,package)
                    if not spec:
                        raise ModuleNotFoundError(f"No module named {module_name}")
                    package_path.append(e)

                return IZaberSpec(spec,module_name)
            except ImportError:
                return

        return

    def find_module(self, module_name, package_path=None):
        # Only respond to izaber.* modules
        try:
            if module_name.index('izaber.') != 0:
                return
        except:
            return

        for prefix in self.prefixes:
            try:
                if module_name.index(prefix) != 0:
                    continue
            except ValueError:
                continue
            loader = self.attempt_load(prefix,module_name)
            if loader:
                return loader

        # Couldn't find it!
        return

import traceback

from izaber.startup import initialize, app_config
from izaber.zconfig import config

"""
This module does some magic! Without the following code it would
not be able to share the izaber.* namespace.

What we do here is intercept the request for any "import"
statement that starts with "izaber". If it does, it attempts to
rewrite the import attempt to izaber_WHATEVERTHENEXTELEMENTWAS

Then if it manages to find and load it okay, it will then pass
the loaded import onto to the rest of the system under the
izaber.* namespace for usage by developers.

If a submodule should also serve as the base point for additional
submodules, be sure to include a call to add_prefix. For instance,
if izaber.foo should allow the loading of izber.foo.bar via
izaber_foo_bar, then ensure that izaber_foo/__init__.py contains
the following code:

import izaber
izaber.autoloader.add_prefix('izaber_foo')

For another example have a look at izaber.wamp (which allows the
load of izaber.wamp.fuse)

"""


autoloader = IZaberFinderImportlib()
sys.meta_path.insert(0, autoloader)


