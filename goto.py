import functools
import inspect
import re
import sys
import trace


def allow_goto(fn):
    @functools.wraps(fn)
    def anon(*args, **kwargs):
        oldtrace = sys.gettrace()
        sys.settrace(trace_calls)
        value = fn(*args, **kwargs)
        sys.settrace(oldtrace)
        return value
    return anon


def trace_calls(frame, event, arg):
    return handle_goto_lines


def handle_goto_lines(frame, event, arg):
    source, start_line = inspect.getsourcelines(frame.f_code)
    jumps = fetch_jumps(tuple(source), start_line)

    if frame.f_lineno in jumps:
        frame.f_lineno = jumps[frame.f_lineno]


@functools.lru_cache()
def fetch_jumps(source, start_line):
    gotos = {}
    labels = {}

    for lineno, line in enumerate(source, start_line):
        match = re.match(r" *(?P<label>\w+): (?P<command>goto|label)\b", line)
        if match:
            label_info = match.groupdict()
            if label_info['command'] == 'goto':
                gotos[label_info['label']] = lineno
            else:
                labels[label_info['label']] = lineno

    extras = gotos.keys() - labels.keys()
    if extras:
        first = next(iter(extras))
        lineno = gotos[first]
        line = source[lineno - start_line]
        column = next(i for i, c in enumerate(line) if c != ' ')
        # XXX: __file__ isn't right
        raise SyntaxError(f"label {first!r} is not defined.", (__file__, lineno, column, line))

    return {
        lineno: labels[label]
        for label, lineno in gotos.items()
    }


# ---

if __name__ == '__main__':
    @allow_goto
    def sample(a, b):
        i = 0
        foo: label = 0
        i = i + 1
        print("iter:", i)
        if i <= 10:
            foo: goto = 0

    sample(3, 2)
