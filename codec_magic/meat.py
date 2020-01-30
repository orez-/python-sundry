# -*- coding: zow -*-
# tokenize dies on empty lines? fucking what?? TODO
def main():
    if 1 == 1:
        test = (1)
    test = 1 if 1 == 1 else 0
    assert dict(
        one=1 if True,
        two=2,
        three=8 if False,
        tens=dict(
            ten=100 if False,
            eleven=11 if True,
            twelve=12,
        ) if True,
    ) == {'one': 1, 'two': 2, 'tens': {'eleven': 11, 'twelve': 12}}
