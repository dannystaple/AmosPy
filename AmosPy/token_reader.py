import struct
from AmosPy.amosTokens import token_map

__author__ = 'danny'


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