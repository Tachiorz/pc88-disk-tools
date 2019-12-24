import sys
import struct


n88tokens = {
    0x80: 'AUTO',
    0xF8: 'AND',
    0x10: 'ABS',
    0x11: 'ATN',
    0x12: 'ASC',
    0x13: 'ATTR$',
    0x4C: 'AKCNV$',
    0x81: 'BSAVE',
    0x82: 'BLOAD',
    0x83: 'BEEP',
    0x84: 'CONSOLE',
    0x85: 'COPY',
    0x86: 'CLOSE',
    0x87: 'CONT',
    0x88: 'CLEAR',
    0x14: 'CSRLIN',
    0x15: 'CINT',
    0x16: 'CSNG',
    0x17: 'CDBL',
    0x18: 'CVI',
    0x19: 'CVS',
    0x1A: 'CVD',
    0x1B: 'COS',
    0x1C: 'CHR$',
    0x89: 'CALL',
    0x8A: 'COMMON',
    0x8B: 'CHAIN',
    0x8C: 'COM',
    0x8D: 'CIRCLE',
    0x8E: 'COLOR',
    0x8F: 'CLS',
    0xE8: 'CMD',
    0x90: 'DELETE',
    0x91: 'DATA',
    0x92: 'DIM',
    0x93: 'DEFSTR',
    0x94: 'DEFINT',
    0x95: 'DEFSNG',
    0x96: 'DEFDBL',
    0x97: 'DSKO$',
    0x98: 'DEF',
    0x41: 'DSKI$',
    0x1D: 'DSKF',
    0x00: 'DATE$',
    0xA2: 'DRAW',
    0x99: 'ELSE',
    0x9A: 'END',
    0x9B: 'ERASE',
    0x9C: 'EDIT',
    0x9D: 'ERROR',
    0x1E: 'ERL',
    0x1F: 'ERR',
    0x20: 'EXP',
    0x21: 'EOF',
    0xFB: 'EQV',
    0x9E: 'FOR',
    0x9F: 'FIELD',
    0xA0: 'FILES',
    0xA1: 'FN',
    0x42: 'FRE',
    0x22: 'FIX',
    0x23: 'FPOS',
    0xA3: 'GOTO',
    0xA4: 'GOSUB',
    0xA5: 'GET',
    0x24: 'HEX$',
    0xA6: 'HELP',
    0x44: 'INPUT$',
    0xA7: 'INPUT',
    0xA8: 'IF',
    0x25: 'INSTR',
    0x26: 'INT',
    0x27: 'INP',
    0xFC: 'IMP',
    0x28: 'INKEY$',
    0x4E: 'IEEE',
    0xE9: 'IRESET',
    0xEA: 'ISET',
    0x45: 'JIS$',
    0xA9: 'KEY',
    0xAA: 'KILL',
    0xAB: 'KANJI',
    0xE6: 'KINPUT',
    0x46: 'KNJ$',
    0x47: 'KTYPE',
    0x48: 'KLEN',
    0x49: 'KMID$',
    0x4A: 'KEXT$',
    0x4B: 'KINSTR',
    0x4D: 'KACNV$',
    0xEE: 'KPLOAD',
    0xAC: 'LOCATE',
    0xAD: 'LPRINT',
    0xE3: 'LIST',
    0xAE: 'LLIST',
    0x29: 'LPOS',
    0xAF: 'LET',
    0xB0: 'LINE',
    0xB1: 'LOAD',
    0xB2: 'LSET',
    0xB3: 'LFILES',
    0x2A: 'LOG',
    0x2B: 'LOC',
    0x2C: 'LEN',
    0x2D: 'LEFT$',
    0x2E: 'LOF',
    0xB4: 'MOTOR',
    0xB5: 'MERGE',
    0xFD: 'MOD',
    0x2F: 'MKI$',
    0x30: 'MKS$',
    0x31: 'MKD$',
    0x01: 'MID$',
    0xB6: 'MON',
    0x32: 'MAP',
    0xB7: 'NEXT',
    0xB8: 'NAME',
    0xB9: 'NEW',
    0xBA: 'NOT',
    0xBB: 'OPEN',
    0xBC: 'OUT',
    0xBD: 'ON',
    0xF9: 'OR',
    0x33: 'OCT$',
    0xBE: 'OPTION',
    0xBF: 'OFF',
    0xC0: 'PRINT',
    0xC1: 'PUT',
    0xC2: 'POKE',
    0x34: 'POS',
    0x35: 'PEEK',
    0xC3: 'PSET',
    0xC4: 'PRESET',
    0x02: 'POINT',
    0xC5: 'PAINT',
    0x03: 'PEN',
    0xEB: 'POLL',
    0xC6: 'RETURN',
    0xC7: 'READ',
    0xC8: 'RUN',
    0xC9: 'RESTORE',
    0xFF: 'REM',
    0xCB: 'RESUME',
    0xCC: 'RSET',
    0x36: 'RIGHT$',
    0x37: 'RND',
    0xCD: 'RENUM',
    0xCE: 'RANDOMIZE',
    0xCF: 'ROLL',
    0xEC: 'RBYTE',
    0xD0: 'SCREEN',
    0x38: 'SEARCH',
    0xD1: 'STOP',
    0xD2: 'SWAP',
    0xD3: 'SAVE',
    0xD4: 'SPC',
    0xD5: 'STEP',
    0x39: 'SGN',
    0x3A: 'SQR',
    0x3B: 'SIN',
    0x3C: 'STR$',
    0x3D: 'STRING$',
    0x3E: 'SPACE$',
    0xE4: 'SEG',
    0xE5: 'SET',
    0x4F: 'STATUS',
    0xE7: 'SRQ',
    0xD6: 'THEN',
    0xD7: 'TRON',
    0xD8: 'TROFF',
    0xD9: 'TAB',
    0xDA: 'TO',
    0x3F: 'TAN',
    0xDB: 'TERM',
    0x04: 'TIME$',
    0xDC: 'USING',
    0xDD: 'USR',
    0x40: 'VAL',
    0x05: 'VIEW',
    0x43: 'VARPTR',
    0xDE: 'WIDTH',
    0x06: 'WINDOW',
    0xDF: 'WAIT',
    0xE0: 'WHILE',
    0xE1: 'WEND',
    0xE2: 'WRITE',
    0xED: 'WBYTE',
    0xFA: 'XOR',
    0xF3: '+',
    0xF4: '-',
    0xF5: '*',
    0xF6: '/',
    0xF7: '^',
    0xFE: '\\',
    0xF0: '>',
    0xF1: '=',
    0xF2: '<',
}

n88_unicode_table = {
    0x80: 0x02581,
    0x81: 0x02582,
    0x82: 0x02583,
    0x83: 0x02584,
    0x84: 0x02585,
    0x85: 0x02586,
    0x86: 0x02587,
    0x87: 0x02588,
    0x88: 0x0258F,
    0x89: 0x0258E,
    0x8a: 0x0258D,
    0x8b: 0x0258C,
    0x8c: 0x0258B,
    0x8d: 0x0258A,
    0x8e: 0x02589,
    0x8f: 0x0253C,
    0x90: 0x02534,
    0x91: 0x0252C,
    0x92: 0x02524,
    0x93: 0x0251C,
    0x94: 0x02594,
    0x95: 0x02500,
    0x96: 0x02502,
    0x97: 0x02595,
    0x98: 0x0250C,
    0x99: 0x02510,
    0x9a: 0x02514,
    0x9b: 0x02518,
    0x9c: 0x025DC,
    0x9d: 0x025DD,
    0x9e: 0x025DF,
    0x9f: 0x025DE,
    0xa0: 0x025A0,  # space replacement
    0xe0: 0x02550,
    0xe1: 0x0255E,
    0xe2: 0x0256A,
    0xe3: 0x02561,
    0xe4: 0x025E2,
    0xe5: 0x025E3,
    0xe6: 0x025E5,
    0xe7: 0x025E4,
    0xe8: 0x02660,
    0xe9: 0x02665,
    0xea: 0x02666,
    0xeb: 0x02663,
    0xec: 0x025CF,
    0xed: 0x025CB,
    0xee: 0x02571,
    0xef: 0x02572,
    0xf0: 0x02573,
    0xf1: 0x0E001,
    0xf2: 0x0E002,
    0xf3: 0x0E003,
    0xf4: 0x0E004,
    0xf5: 0x0E005,
    0xf6: 0x0E006,
    0xf7: 0x0E007,
}

n88_2byte_unicode_table = {
    0x242C: 0xF242C,
}

def n88basic_to_utf8(txt):
    out = b""
    jis = b""
    is_jis = False
    i = 0
    while True:
        if i < len(txt)-1 and txt[i] == 0x1b and txt[i + 1] == 0x4b:  # switch to 16bit encoding:
            i += 2
            is_jis = True
            jis = b""
        elif i < len(txt)-1 and txt[i] == 0x1b and txt[i + 1] == 0x48:  # switch to 8bit
            is_jis = False
            jis2 = ""
            for j in range(0,len(jis), 2):
                code = struct.unpack('<H', jis[j:j+2])[0]
                try:
                    bcode = struct.pack('<H', code & 0x7FFF)  # todo: why is that?
                    bcode = bytes([0x1b, 0x24, 0x42]) + bcode + bytes([0x1b, 0x28, 0x42])
                    jis2 += bcode.decode('iso2022_jp_ext')
                except:
                    # todo: this is getting ridiculous
                    print("Unknown character:", hex(code))
                    jis2 += chr(0x0F0000 & code)
            jis = jis2
            out += jis.encode('utf8')
            i += 2
        else:
            if is_jis is True:
                jis += txt[i:i + 2]
                i += 2
            else:
                if txt[i] in n88_unicode_table:
                    out += chr(n88_unicode_table[txt[i]]).encode('utf-8')
                else:
                    b = bytes([txt[i]])
                    out += b.decode('shift-jis').encode('utf-8')
                i += 1
                if i == len(txt): break
    return out


def mbf2ieee(mbf_4bytestring):
    """
    https://stackoverflow.com/questions/2268191/how-to-convert-from-ieee-python-float-to-microsoft-basic-float
    """
    msbin = struct.unpack('4B', mbf_4bytestring)
    if msbin[3] == 0: return 0.0
    ieee = [0] * 4
    sign = msbin[2] & 0x80
    ieee_exp = msbin[3] - 2
    ieee[3] = sign | (ieee_exp >> 1)
    ieee[2] = (ieee_exp << 7) & 0xFF | (msbin[2] & 0x7f)
    ieee[:2] = msbin[:2]
    return struct.unpack('f', bytes(ieee))[0]


def msd2float(msd):
    # take out values that don't make sense possibly the NaN and Infinity
    if sum(msd) in [0, 72, 127]:
        return 0.0
    b = msd[:]
    sign = msd[-2] & 0x80
    b[-2] |= 0x80  # hidden most sig bit in place of sign
    exp = msd[-1] - 0x80 - 56  # exponent offset
    acc = 0
    for i, byte in enumerate(b[:-1]):
        acc |= byte << (i*8)
    return (float(acc)*2.0**exp)*((1., -1.)[sign != 0])


def detokenize(buf):
    """
    Detokenize N88 BASIC bytecode
    (This is complete guesswork)
    :param buf: binary basic data
    :return: decompiled basic text
    """
    idx = 0
    txt = b""
    while True:
        if idx >= len(buf): break
        length = struct.unpack('<H', buf[idx:idx+2])[0]
        if length == 0: break
        line_num, data = struct.unpack("<H{}s".format(length - 4), buf[idx+2:idx+length])
        idx += length
        if line_num == 0:
            break
        cmd = b''
        i = 0
        while True:
            if i == len(data): break
            b = data[i]
            i += 1
            # constant tokens are partially borrowed from http://www.chebucto.ns.ca/~af380/GW-BASIC-tokens.html
            # todo: confirm constant tokens
            if b == 0:  # comment, end of line
                cmd += data[i:-1]
                break
            elif b > 0 and b < 10:  # spaces
                cmd += b' ' * b
            elif b >= 0x10 and b <= 0x19:  # number 0..9
                cmd += bytes([b+0x20])
            elif b == 0x0B:  # octal
                val = struct.unpack("<H", data[i:i + 2])[0]
                cmd += "&O{:o}".format(val).encode('ascii')
                i += 2
            elif b == 0x0C:  # hex word
                val = struct.unpack("<H", data[i:i + 2])[0]
                cmd += "&H{:X}".format(val).encode('ascii')
                i += 2
            elif b == 0x0D or b == 0x0E:  # line number
                cmd += str(struct.unpack("<H", data[i:i+2])[0]).encode('ascii')
                i += 2
            elif b == 0x0F:  # byte
                cmd += str(data[i]).encode('ascii')
                i += 1
            elif b == 0x1C:  # word
                cmd += str(struct.unpack("<H", data[i:i+2])[0]).encode('ascii')
                i += 2
            elif b == 0x1D:  # four-byte single-precision floating-point
                f = mbf2ieee(data[i:i+4])
                cmd += "{:f}".format(f).rstrip('0').rstrip('.').encode('ascii')
                i += 4
            elif b == 0x1F:  # eight-byte double-precision floating-point
                d = msd2float(data[i:i+8])
                cmd += "{:f}".format(d).rstrip('0').rstrip('.').encode('ascii')
                i += 8
            elif b >= ord('A') and b <= ord('z') and data[i] >=0 and data[i] <= 0x20:  # variable?
                cmd += bytes([b])
                varlen = data[i]
                if varlen > 0:
                    cmd += struct.unpack("{}s".format(varlen), data[i+1:i+varlen+1])[0]
                i += varlen + 1
            elif b == ord('"'):  # string
                cmd += b'"'
                while data[i] != ord('"'):  # look for closing "
                    if data[i] == 0x1b:  # switch encoding
                        while True:
                            cmd += bytes([data[i]])
                            i += 1
                            if data[i] == 0x1b: break
                    cmd += bytes([data[i]])
                    i += 1
                    if data[i] == 0: break
                if data[i] == 0: break
                cmd += b'"'
                i += 1
            elif chr(b) in (':', ';', ',', '*', '#', '$', '%', '(', ')'):
                if data[i] != 0x99:  # ELSE stored with invisible colon, 3A, before it
                    cmd += bytes([b])
            elif b == 0x91:
                cmd += b"DATA"
                cmd += data[i:-1]
                break
            elif b == 0xFF:  # function
                b = data[i]
                i += 1
                if b-0x80 in n88tokens:
                    cmd += bytes(n88tokens[b-0x80].encode('ascii'))
                else: print("line {}: unknown function {:X}".format(line_num, b))
            elif b in n88tokens:
                cmd += bytes(n88tokens[b].encode('ascii'))
            else:
                print("line {}: unknown token {:X}".format(line_num, b))
        line = str(line_num).encode('ascii')
        if cmd[0] != 0x20: line += b' '
        line += cmd
        txt += line + b'\x0d\x0a'
    return txt


if __name__ == '__main__':
    with open(sys.argv[1], 'rb') as f:
        detokenize(f.read())
