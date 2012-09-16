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

#Given majority have no extra, perhaps simply having a tuple of length 1 only means the same?
token_map = {
    0x0000: (None,),
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
    0x005c: (',',),
    0x0054: (';',),#Statement semicolon
    0x0064: (';',),#Print/input semicolon
    0x0074: ('(',),
    0x007c: (')',),
    0x0094: ('To',), #For n=blah TO blah
    0x00f2: ('Inkey$',),
    0x019c: ('Every On',),
    0x01dc: ('Asc',),
    0x023C: ('For', unknownExtra),
    0x0246: ('Next',),
    0x0250: ('Repeat', unknownExtra),
    0x025c: ('Until',),
    0x0268: ('While', unknownExtra),
    0x0274: ('Wend',),
    0x027E: ('Do', unknownExtra),
    0x0286: ('Loop',),
    0x02a8: ('Goto',),
    0x02b2: ('Gosub',),
    0x02BE: ('If', unknownExtra),
    0x02c6: ('Then',),
    0x02D0: ('Else', unknownExtra),
    0x02da: ('EndIf',),
    0x0290: ('Exit If',),
    0x029E: ('Exit',),
    0x0316: ('On',),
    0x034a: ('Every',),
    0x0356: ('Step',),
    0x0360: ('Return',),
    0x036c: ('Pop',),
    0x0376: ('Procedure', readProcedure),
    0x0386: ('Proc',),
    0x0390: ('End Proc',),
    0x03b6: ('End',),
    0x0404: ('Data', unknownExtra),
    0x040e: ('Read',),
    0x0436: ('Break On',),
    0x0426: ('Break Off',),
    0x0444: ('Inc',),
    0x044e: ('Dec',),
    0x0458: ('Add',),
    0x0476: ('Print',),
    0x04d0: ('Input',),
    0x050e: ('Mid$',),
    0x0528: ('Left$', None),
    0x0536: ('Right$', None),
    0x0546: ('Flip$', None),
    0x0552: ('Chr$', None),
    0x055e: ('Space$', None),
    0x056c: ('String$', None),
    0x057c: ('Upper$', None),
    0x058a: ('Lower$', None),
    0x0598: ('Str$', None),
    0x05a4: ('Val', None),
    0x05e4: ('Instr$', None),
    0x05da: ('Len', None),
    0x0640: ('Dim', None),
    0x064A: ('Rem', readRem),
    0x0652: ('Rem', readRem),
    0x0658: ('Sort', None),
    0x0670: ('Edit', None), #Returns to the editor
    0x067a: ('Direct', None),
    0x0686: ('Rnd', None),
    0x09ea: ('InitScreen', None),
    0x0c52: ('X Text', None),
    0x0c60: ('Y Text', None),
    0x0cfc: ('Palette', None),
    0x0d0a: ('Border', None),
    0x0e3c: ('Plot', None),
    0x0e74: ('Line', None),
    0x0e86: ('Ellipse', None),#Drawing an ellipse
    0x0e9a: ('Circle', None),
    0x0eac: ('Polyline to', None),
    0x0ec8: ('Fill Box', None),#Drawing a box
    0x0ed8: ('Box', None),
    0x0ee8: ('Paint', None),
    0x0f4a: ('Text', None),
    0x1034: ('Set Line', None),
    0x1044: ('Ink', None),#Gr Ink
    0x1066: ('Gr Writing', None),
    0x129e: ('Sleep', None),
    0x1378: ('Locate', None),
    0x13ac: ('Pen$', None),
    0x13b8: ('Paper$', None),
    0x13c6: ('At', None),
    0x13d2: ('Paper', None),
    0x13dc: ('Pen', None), #Note - 13d2/13da may be reversed.
    0x13e8: ('Print', None), #Why have I found 2 prints? - in usage, this one is used where there is an expression,
                             # the other is used only with consts...
    0x1408: ('Writing', None),
    0x1462: ('Inverse Off', None),
    0x1474: ('Inverse On', None),
    0x14a2: ('Shade Off', None),
    0x14b2: ('Shade On', None),
    0x1484: ('Under Off', None),
    0x1494: ('Under On', None),
    0x157c: ('CMove', None),
    0x16e2: ('Mouse Key', None),
    0x1e32: ('Mouse Click', None),
    0xff4c: ('Or', None),
    0xff58: ('And', None),
    0xffc0: ('+', None),#TkEg O22
    0xffe2: ('*', None),#TkM O00
    0xffa2: ('=', None),#TkEg o20
    0xffac: ('<', None),
    0xffb6: ('>', None),#TkEg o20
    0xffca: ('-', None), #Unary negation or both?
    0x0bae: ('Clear', None),
}
