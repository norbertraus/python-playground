from weakref import WeakValueDictionary


class Foo:

    # creates instance of the class
    def __new__(cls, *args, **kwargs):
        """
        __new__() is intended mainly to allow subclasses of immutable types (like int, str, or tuple)
        to customize instance creation.
        It is also commonly overridden in custom metaclasses in order to customize class creation.

        """
        instance = super(Foo, cls).__new__(cls)
        return instance

    def __init__(self):
        print("Initialized")


f = Foo()
assert f is not None


class Foo_without_init_invoked:

    def __new__(cls, *args, **kwargs):
        instance = super(Foo_without_init_invoked, cls).__new__(cls)

        # not returning instance

    def __init__(self):
        assert False


f = Foo_without_init_invoked()  # no init will be invoked
assert f is None


# it could be useful to have caching instance constructor with some form of identity

class Foo_with_caching:
    _foo_cache = WeakValueDictionary()

    def __new__(cls, id, *args, **kwargs):
        instance = cls._foo_cache.get(id)

        if instance is None:
            instance = cls._foo_cache[id] = (
                super(Foo_with_caching, cls)
                    .__new__(cls)
                    ._init(id=id)
            )

        return instance

    def __init__(self, *args, **kwargs):
        # it will be sorted by the caching __new__
        pass

    def _init(self, id):
        self.id = id

        return self


f1 = Foo_with_caching(1)
assert f1.id == 1

f2 = Foo_with_caching(2)
assert f2.id == 2
assert f1 is not f2

f1_prime = Foo_with_caching(1)
assert f1_prime.id == 1
assert f1_prime is f1
