class Singleton(object):
    _instances = {}

    def __new__(self, *args, **kwargs):
        if self not in self._instances:
            self._instances[self] = \
                super(Singleton, self).__new__(self, *args, **kwargs)
        return self._instances[self]
# def singleton(cls):
#     instances = {}
#     def getinstance():
#         if cls not in instances:
#             instances[cls] = cls()
#         return instances[cls]
#     return getinstance
