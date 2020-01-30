import codecs
import re


encode = codecs.utf_8_encode

swap_sign = {'-': '+', '+': '-'}.__getitem__


def xpp_translate(match):
    sign = match[2][0]
    back = swap_sign(sign)
    return f"(({match[1]}:={match[1]}{sign}1){back}1)"


def decode(input, errors='strict'):
    file_bytes = input.tobytes().split(b'\n')
    # Replace the first line with an encoding that isn't this one to avoid RecursionError.
    # Gross!
    file_bytes[0] = b'# -*- coding: utf-8 -*-'

    ppx = re.compile(r"(\+\+|\-\-)([a-z_]\w*)")
    xpp = re.compile(r"([a-z_]\w*)(\+\+|\-\-)")
    file_bytes = [
        xpp.sub(
            xpp_translate,
            ppx.sub(lambda m: f"({m[2]}:={m[2]}{m[1][0]}1)", line.decode('utf8'))
        )
        for line in file_bytes
    ]
    return '\n'.join(file_bytes), 0


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
    if name == 'plusplus':
        return codecs.CodecInfo(
            name='plusplus',
            encode=encode,
            decode=decode,
            incrementalencoder=IncrementalEncoder,
            incrementaldecoder=IncrementalDecoder,
            streamreader=StreamReader,
            streamwriter=StreamWriter,
        )


codecs.register(getregentry)
