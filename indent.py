import contextlib
import functools

def indent(print_fn):
    def indent_print(*args, **kwargs):
        print(end='    ')
        print_fn(*args, **kwargs)

    def decorator(fn):
        fn(indent_print)
    return decorator


print("{")
@indent(print)
def _indent(print):
    print('"wow": {')
    @indent(print)
    def _indent(print):
        print('"dang": 5')
    print('}')
print('}')


# original_print = print
# def _indent_print(print):
#     @functools.wraps(print)
#     def anon(*args, **kwargs):
#         original_print(end='    ')
#         print(*args, **kwargs)
#     return anon


# @contextlib.contextmanager
# def indent(print):
#     yield _indent_print(print)


# print("{")
# with indent(print) as print:
#     print('"wow": {')
#     with indent(print) as print:
#         print('"dang": 5')
#     print('}')
# print('}')

