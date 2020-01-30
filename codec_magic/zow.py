# Zow! Web access!

import codecs
import tokenize


encode = codecs.utf_8_encode

def decode(input, errors='strict'):
    import pprint
    file_bytes = input.tobytes().split(b'\n')
    # Replace the first line with an encoding that isn't this one to avoid RecursionError.
    # Gross!
    file_bytes[0] = b'# -*- coding: utf-8 -*-'
    print(file_bytes)
    file_bytes_iter = iter(file_bytes)

    token_gen = tokenize.tokenize(lambda: next(file_bytes_iter))
    pprint.pprint(list(token_gen))
    return ("""main = lambda: print("You're not done yet dick monkey.")""", 0)
    # return codecs.utf_8_decode(input, errors, True)

class IncrementalEncoder(codecs.IncrementalEncoder):
    def encode(self, input, final=False):
        return codecs.utf_8_encode(input, self.errors)[0]

class IncrementalDecoder(codecs.BufferedIncrementalDecoder):
    _buffer_decode = codecs.utf_8_decode

class StreamWriter(codecs.StreamWriter):
    encode = codecs.utf_8_encode

class StreamReader(codecs.StreamReader):
    decode = codecs.utf_8_decode


def getregentry(name):
    if name == 'zow':
        return codecs.CodecInfo(
            name='zow',
            encode=encode,
            decode=decode,
            incrementalencoder=IncrementalEncoder,
            incrementaldecoder=IncrementalDecoder,
            streamreader=StreamReader,
            streamwriter=StreamWriter,
        )


codecs.register(getregentry)



# dict(
#     foo=bar if baz,
#     bang=bazinga,
# )

# zow.conditional_apply(
#     dict,
#     foo=bar if baz else zow.missing,
#     bang=bazinga,
# )


missing = object()
def conditional_apply(fn, *args, **kwargs):
    return fn(
        *[arg for arg in args if arg is not missing],
        **{key: value for key, value in kwargs.items() if value is not zow.missing}
    )
