from __future__ import print_function
import struct
import sys
from amosTokens import token_map
__author__ = 'stapled'
from extensions import extensions_table


def baseN(num,b,numerals="0123456789abcdefghijklmnopqrstuvwxyz"):
    return ((num == 0) and  "0" ) or ( baseN(num // b, b).lstrip("0") + numerals[num % b])


def readHeader(byteStream):
    version = struct.unpack('16s', byteStream.read(16))[0]
    nBytes = struct.unpack('>I', byteStream.read(4))[0]
    return {'version':version, 'length':nBytes}


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
                raise BadTokenRead("Read %d bytes, expected %d. So far: \n%s" % (bytesRead, lineLength, repr(tokensRead)))
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
    'DecVal':   lambda data: "%d" % data,
    'HexVal':   lambda data: "0x%x" % data,
    'BinVal':   lambda data: baseN(data, 2),
    'Dbl Str':  lambda data: '"%s"' % data,
    'Variable': lambda data: data,
    'Goto Label Ref': lambda data: data,
    'Label':    lambda data: "Label %s:" % data,
    'Extension':extension_str,
    'Procedure':procedure_str,
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


def convert_file(filename):
    """Output a single amos tokenised file as text"""
    tr = TokenReader()
    byteStream = open(filename,"rb")
    header = readHeader(byteStream)
    bytesRead = 0
    lines = []
    while bytesRead < header['length']:
        inBytesRead, indentLevel, tokensRead = tr.readTokenisedLine(byteStream)
        bytesRead += inBytesRead
        lines.append((indentLevel, tokensRead))

    return lines, tr.unknown_tokens, bytesRead, header


def printLine(indentLevel, tokensRead):
    print(indentLevel * ' ', ' '.join(tokenToStr(*token) for token in tokensRead))


def output_converted(lines, unknown_tokens, bytes_read, header):
    print(header)
    [printLine(indent_level, tokens_read) for indent_level, tokens_read in lines]
    print("Code Bytes read", bytes_read, "of", header['length'])
    if unknown_tokens:
        print("Found %d unknown tokens" % unknown_tokens)
    else:
        print("All tokens translated")


if __name__ == '__main__':
    output_converted(*convert_file(sys.argv[1]))

