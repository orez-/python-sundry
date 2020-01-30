import pytest

import main


def _space_prefix_lengths(lines):
    for line in lines:
        for i, elem in enumerate(line):
            if elem != ' ':
                yield i
                break


def format_docstring(docstr):
    docstr = docstr.strip('\n')
    lines = docstr.split('\n')
    prefix_length = min(_space_prefix_lengths(lines))
    return '\n'.join(
        line[prefix_length:]
        for line in lines
    )


@pytest.mark.parametrize("input_,output", [
    (
        """
        +-++++++++
        +-++++++++
        +-++++++++
        +-----++++
        +-+++-++++
        +-+++-++++
        +++++-++++
        ++------++
        +++++-++++
        +++++-++++
        LONDON;DELHI;ICELAND;ANKARA
        """,
        """
        +L++++++++
        +O++++++++
        +N++++++++
        +DELHI++++
        +O+++C++++
        +N+++E++++
        +++++L++++
        ++ANKARA++
        +++++N++++
        +++++D++++
        """
    ),
    (
        """
        +-++++++++
        +-++++++++
        +-------++
        +-++++++++
        +-++++++++
        +------+++
        +-+++-++++
        +++++-++++
        +++++-++++
        ++++++++++
        AGRA;NORWAY;ENGLAND;GWALIOR
        """,
        """
        +E++++++++
        +N++++++++
        +GWALIOR++
        +L++++++++
        +A++++++++
        +NORWAY+++
        +D+++G++++
        +++++R++++
        +++++A++++
        ++++++++++
        """
    )
])
def test(input_, output):
    input_ = format_docstring(input_)
    output = format_docstring(output)

    input_iter = iter(input_.split('\n'))
    main.input = lambda: next(input_iter)

    assert main.main() == output
