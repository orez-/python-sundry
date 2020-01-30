import functools


def spooky_scurry(**kwargs):
    (key, transform), = kwargs.items()

    def decorator(fn):
        @functools.wraps(fn)
        def _inner(*args, **kwargs):
            if not args and not kwargs:
                return fn(**{key: _inner.values})

            _inner.values.append(transform(*args, **kwargs))
            return _inner
        _inner.values = []
        return _inner
    return decorator


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
    (facility_id='wait', bucket_id='oh', party_id='shit')
)()
