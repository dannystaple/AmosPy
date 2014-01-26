"""Core conversion of AMOS tokens to text"""
import struct
from AmosPy.extensions import extensions_table
from AmosPy.token_reader import TokenReader


def baseN(num, b, numerals="0123456789abcdefghijklmnopqrstuvwxyz"):
    return ((num == 0) and "0") or (baseN(num // b, b).lstrip("0") + numerals[num % b])


def readHeader(byteStream):
    version = struct.unpack('16s', byteStream.read(16))[0]
    nBytes = struct.unpack('>I', byteStream.read(4))[0]
    return {'version': version, 'length': nBytes}


def extension_str(data):
    extNo, token = data
    if extNo in extensions_table and token in extensions_table[extNo]:
        return extensions_table[extNo][token]
    else:
        return "[Extension %d : 0x%04x]" % data


def procedure_str(data):
    output = 'Procedure'
    if data['flags']:
        output += ' <%s>' % repr(data['flags'])
    return output


def tokenToStr(tokenName, tokenData):
    token_output_formats = {
        'DecVal': lambda data: "%d" % data,
        'HexVal': lambda data: "0x%x" % data,
        'BinVal': lambda data: baseN(data, 2),
        'Dbl Str': lambda data: '"%s"' % data,
        'Variable': lambda data: data,
        'Goto Label Ref': lambda data: data,
        'Label': lambda data: "Label %s:" % data,
        'Extension': extension_str,
        'Procedure': procedure_str,
        }

    output = ''
    if tokenName:
        if tokenName in token_output_formats:
            output = token_output_formats[tokenName](tokenData)
        else:
            output += tokenName
            if tokenData is not None:
                output += " " + repr(tokenData)

    return str(output)


class Converter(object):
    def __init__(self):
        self.bytes_read = 0
        self.unknown_tokens = 0

    def do_file(self, filename):
        """Convert a file into lines of text.
        Note the file header is the first item yielded,
        then plain text after that."""
        tr = TokenReader()
        byteStream = open(filename, "rb")
        header = readHeader(byteStream)
        yield header
        self.bytes_read = 0
        while self.bytes_read < header['length']:
            inBytesRead, indentLevel, tokensRead = tr.readTokenisedLine(byteStream)
            self.bytes_read += inBytesRead
            line = indentLevel * ' ' + ' '.join(tokenToStr(*token) for token in tokensRead)
            yield line
        self.unknown_tokens = tr.unknown_tokens