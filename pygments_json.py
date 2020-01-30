import json

import pygments
import pygments.formatters
import pygments.lexers


def format_dict_for_terminal(data):
    return pygments.highlight(
        json.dumps(data, indent=2, sort_keys=True, default=str),
        pygments.lexers.JsonLexer(),
        pygments.formatters.TerminalFormatter(),
    )
