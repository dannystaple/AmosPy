"""Amos had a number of extension modules.
This is a table of extensions I've seen,
along with their tokens.
"""
extensions_table = {
    1: {
        0x0012: 'Vumeter',
        0x0020: 'Voice',
        0x002c: 'Music Stop',
        0x004c: 'Tempo',
        0x0058: 'Music',
        0x0074: 'Boom',
        0x007e: 'Shoot',
        0x00f8: 'Sam Play',
        0x00de: 'Sam Play',
        0x0118: 'Bell',
        0X0144: 'Play',
        0x0196: 'Mvolume',
        0x01a4: 'Volume',
        0x01ca: 'Led On',
        0x01d6: 'Led Off',
        0x01e4: 'Say',
        0x01fa: 'Set Talk',
        0x0256: 'Sam Stop',
        0x025e: 'Track Stop',
        0x026e: 'Track Loop On',
        0x0282: 'Track Loop Of', # This is actually a typo in AMOS!
        0x0296: 'Track Play',
        0x02a8: 'Track Play',
        0x02ba: 'Track Load'
    },
    2: {
        0x0006: 'Pack',
        0x0026: 'Spack',
        0x0036: 'Spack',
        0x0048: 'Unpack',
        0x0056: 'Unpack'
    },
    3: {
        0x0006: 'Request On',
        0x0028: 'Request Wb',
    },
    5: {
        0x0028: 'Comp Test On',
        0x003a: 'Comp Test Off'
    },
    6: {
        0x0006: 'Serial Open',
        0x002c: 'Serial Close',
        0x005e: 'Serial Check',
        0x0072: 'Serial Send',
        0x0100: 'Serial Input$',
    }
}
