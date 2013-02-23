"""Main script of this package - this will convert
an amos tokenised file into plain text, which should be
a representation of what you'd have seen in the Amos editor
window."""
from __future__ import print_function
import struct
import sys
from amosTokens import token_map
from extensions import extensions_table


def baseN(num, b, numerals="0123456789abcdefghijklmnopqrstuvwxyz"):
    return ((num == 0) and "0") or (baseN(num // b, b).lstrip("0") + numerals[num % b])


def readHeader(byteStream):
    version = struct.unpack('16s', byteStream.read(16))[0]
    nBytes = struct.unpack('>I', byteStream.read(4))[0]
    return {'version': version, 'length': nBytes}


class BadTokenRead(Exception):
    pass


class TokenReader(object):
    unknown_tokens = 0

    def readToken(self, byteStream):
        token = struct.unpack('>H', byteStream.read(2))[0]
        bytesRead = 2
        tokenData = None
        try:
            tokenInfo = token_map[token]
            if type(tokenInfo) == str:
                tokenName = tokenInfo
            else:
                if len(tokenInfo) > 1 and tokenInfo[1]:
                    inBytesRead, tokenData = tokenInfo[1](byteStream)
                    bytesRead += inBytesRead
                tokenName = tokenInfo[0]
        except KeyError:
            tokenName = "[Unknown token 0x%04x]" % token
            self.unknown_tokens += 1
            tokenData = None
        return bytesRead, tokenName, tokenData

    def readTokenisedLine(self, byteStream):
        lineLength, indentLevel = struct.unpack('BB', byteStream.read(2))
        lineLength *= 2
        bytesRead = 2
        tokensRead = []
        while bytesRead < lineLength:
            inBytesRead, tokenName, tokenData = self.readToken(byteStream)
            bytesRead += inBytesRead
            tokensRead.append((tokenName, tokenData))
            if bytesRead > lineLength:
                raise BadTokenRead("Read %d bytes, expected %d. So far: \n%s" % (bytesRead,
                                                                                 lineLength, repr(tokensRead)))
            if tokenName is None:
                break
        return bytesRead, indentLevel, tokensRead


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


def tokenToStr(tokenName, tokenData):
    output = ''
    if tokenName:
        if tokenName in token_output_formats:
            output = token_output_formats[tokenName](tokenData)
        else:
            output += tokenName
            if tokenData is not None:
                output += " " + repr(tokenData)

    return output


class Converter(object):
    def __init__(self):
        self.bytes_read = 0
        self.unknown_tokens = 0

    def do_file(self, filename):
        """Convert a file into lines of text"""
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


def convert_file(filename):
    converter = Converter()
    items = converter.do_file(filename)
    header = next(items)
    lines = list(items)
    return lines, converter.unknown_tokens, converter.bytes_read, header


def output_file(filename):
    converter = Converter()
    items = converter.do_file(filename)
    header = next(items)
    try:
        [print(line) for line in items]
    finally:
        print("Code Bytes read", converter.bytes_read, "of", header['length'])
        if converter.unknown_tokens:
            print("Found %d unknown tokens" % converter.unknown_tokens)
    if converter.unknown_tokens == 0 and converter.bytes_read == header['length']:
        print("All tokens translated")


if __name__ == '__main__':
    output_file(sys.argv[1])
