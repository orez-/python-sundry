import functools


class ScurryFn:
    def __init__(self, *, fn, key, transform, values=()):
        self._fn = fn
        self._key = key
        self._transform = transform
        self._values = values

        functools.update_wrapper(self, fn)

    def __call__(self, *args, **kwargs):
        if not args and not kwargs:
            return self._fn(**{self._key: self._values})

        return ScurryFn(
            fn=self._fn,
            key=self._key,
            transform=self._transform,
            values=self._values + (self._transform(*args, **kwargs),),
        )


def spooky_scurry(**kwargs):
    (key, transform), = kwargs.items()

    return lambda fn: ScurryFn(
        fn=fn,
        key=key,
        transform=transform,
    )


@spooky_scurry(ids=lambda *, facility_id, bucket_id, party_id: (facility_id, bucket_id, party_id))
def find_all_by_facility_bucket_party_ids(ids):
    print("!", ids)
    return ids

# ---

result = (
    find_all_by_facility_bucket_party_ids
    (facility_id=1, bucket_id=10, party_id=100)
    (facility_id=2, bucket_id=20, party_id=200)
    (facility_id=3, bucket_id=30, party_id=300)
)()


(
    find_all_by_facility_bucket_party_ids
    (facility_id='can', bucket_id='call', party_id='twice')
)()


# ---

@spooky_scurry(ids=lambda *, self: self ** 2)
def mess(ids):
    print("!", ids)
    return ids

mess(self=1)(self=2)(self=3)(self=4)()
