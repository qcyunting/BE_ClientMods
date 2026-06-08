import mod.client.extraClientApi as clientApi

class Escape(object):
    def __init__(self):
        self.__import_lib = None
        return
    def importModule(self, moduleName):
        if not self.isMinecraftGame():
            return
        else:
            if not self.__import_lib:
                implibObj = None
                for c1 in ('').__class__.__mro__:
                    if c1.__name__ == 'object':
                        implibObj = c1
                        break

                for c2 in implibObj.__subclasses__():
                    if c2.__name__ == '_IterationGuard':
                        implibObj = c2
                        break

                implibObj = implibObj.__init__.__globals__['__builtins__']['__import__']('importlib')
                self.__import_lib = implibObj
            return self.__import_lib.import_module(moduleName)

    @staticmethod
    def isMinecraftGame():
        if clientApi.GetPlatform() is None:
            return False
        else:
            if clientApi.GetPlatform() == -1:
                return False
            return True

instance = Escape()
