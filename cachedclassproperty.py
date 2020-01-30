class cached_classproperty:
    def __init__(self, fget):
        for name in ('__name__', '__module__', '__doc__'):
            setattr(self, name, getattr(fget, name))
        self._fget = fget

    def __get__(self, instance, owner):
        del instance
        value = self._fget(owner)
        setattr(owner, self._fget.__name__, value)
        return value
