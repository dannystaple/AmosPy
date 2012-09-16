import struct

__author__ = 'stapled'
def readRem(byteStream):
    commentLength = struct.unpack('bb', byteStream.read(2))[1]
    bytesRead = 2
    comment = struct.unpack('%ds' % commentLength, byteStream.read(commentLength))[0].rstrip("\x00")
    bytesRead += commentLength
    return bytesRead, comment

def readVal(byteStream):
    intVal = struct.unpack('>i', byteStream.read(4))[0]
    return 4, intVal

def readLabelType(byteStream):
    bytesRead = 0
    unknown, length, flags = struct.unpack("Hbb", byteStream.read(4))
    bytesRead += 4
    name = struct.unpack("%ds" % length, byteStream.read(length))[0].rstrip("\x00")
    bytesRead += length
    return bytesRead, name

def unknownExtra(byteStream):
    byteStream.read(2)
    return 2, None

def readString(byteStream):
    bytesRead = 0
    length = struct.unpack(">h", byteStream.read(2))[0]
    bytesRead += 2
    #Round to next word boundary
    if length % 2:
        length += 1
    data = struct.unpack("%ds" % length, byteStream.read(length))[0].rstrip("\x00")
    bytesRead += length
    return bytesRead, data

def readProcedure(byteStream):
    bytesRead = 0
    bytesToEnd, encSeed, flagsB, encSeed2 = struct.unpack(">ihbb", byteStream.read(8))
    bytesRead += 8
    flags = set()
    if flagsB & 2 ** 7:
        flags.add('folded')
    if flagsB & 2 ** 6:
        flags.add('locked')
    if flagsB & 2 ** 5:
        flags.add('encrypted')
    if flagsB & 2 ** 4:
        flags.add('compiled')
    if 'compiled' in flags:
        byteStream.read(bytesToEnd)
        bytesRead += bytesToEnd
    return bytesRead, {'bytesToEnd': bytesToEnd, 'encSeed': (encSeed, encSeed2), 'flags': flags}

token_map = {
    0x0000: (None, None),
    0x0006: ('Variable', readLabelType),
    0x000C: ('Label', readLabelType),
    0x0012: ('Call', readLabelType),
    0x0018: ('Goto Label Ref', readLabelType),
    0x001E: ('BinVal', readVal),
    0x0026: ('Dbl Str', readString),
    0x002E: ('Sgl Str', readString),
    0x0036: ('HexVal', readVal),
    0x003E: ('DecVal', readVal),
    0x0046: ('Float', None),
    0x004E: ('Extension', None),
    0x005c: (',', None),
    0x0054: (';', None),
    0x0094: ('To', None), #For n=blah TO blah
    0x023C: ('For', unknownExtra),
    0x0246: ('Next', None),
    0x0250: ('Repeat', unknownExtra),
    0x025c: ('Until', None),
    0x0268: ('While', unknownExtra),
    0x027E: ('Do', unknownExtra),
    0x0286: ('[While True]', None),
    0x02BE: ('If', unknownExtra),
    0x02c6: ('Break', unknownExtra),
    0x02D0: ('Else', unknownExtra),
    0x02da: ('EndIf', None),
    0x0290: ('Exit If', None),
    0x029E: ('Exit', None),
    0x0316: ('On', None),
    0x0376: ('Procedure', readProcedure),
    0x0404: ('Data', unknownExtra),
    0x0476: ('Print', None),
    #0x0640: ('[Let]', None) # No - not a let
    0x064A: ('Rem', readRem),
    0x0652: ('Rem', readRem),
    0x09ea: ('InitScreen', None),
    0x0cfc: ('Palette', None),
    0x0d0a: ('Border', None),
    0x0e9a: ('Circle', None),
    0x0ec8: ('Fill Box', None),#Drawing a box
    0x0ed8: ('Box', None),
    0x0e74: ('Line', None),
    0x0e86: ('Ellipse', None),#Drawing an ellipse
    0x0ee8: ('Paint', None),
    0x0eac: ('Polyline to', None),
    0x0f4a: ('Text', None),
    0x1034: ('Set Line', None),
    0x1044: ('Pen Color', None),
    0x1066: ('Gr Writing', None),
    0x129e: ('Sleep', None),
    0x1378: ('Locate', None),
    0x1e32: ('Mouse Click', None),
    0xffc0: ('+', None),
    0xffa2: ('=', None),
    0xffe2: ('*', None),
    0xffb6: ('>', None),
    0x0bae: ('Clear', None)
}
