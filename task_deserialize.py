import datetime
import functools
import inspect

import dateutil.parser


def task_deserialize(fn):
    annotations = dict(fn.__annotations__)
    annotations.pop('return', None)

    @functools.wraps(fn)
    def anon(*args, **kwargs):
        bound_args = inspect.signature(fn).bind(*args, **kwargs)
        for key, type_ in annotations.items():
            if type_ == datetime.datetime:
                bound_args.arguments[key] = dateutil.parser.parse(bound_args.arguments[key])
        return fn(*bound_args.args, **bound_args.kwargs)

    return anon


@task_deserialize
def foo_task(a_datetime: datetime.datetime, an_int: int):
    print(type(an_int), an_int)
    print(type(a_datetime), a_datetime)

# ---

foo_task('2018-07-03T15:01:43.630700', 10)
foo_task(a_datetime='2018-07-03T15:01:43.630700', an_int=10)
