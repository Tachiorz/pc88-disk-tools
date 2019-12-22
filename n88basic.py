import sys
import struct


def decompile(buf):
    """
    Decompile N88 BASIC bytecode
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
            if b == 0:  # comment, end of code?
                cmd += data[i:-1]
                break

            elif b > 0 and b < 10:  # spaces
                cmd += b' ' * b
            elif b >= 0x10 and b <= 0x19:  # number 0..9
                cmd += bytes([b+0x20])
            elif b == 0x0C:  # hex word
                val = struct.unpack("<H", data[i:i + 2])[0]
                cmd += "&H{:X}".format(val).encode('ascii')
                i += 2
            elif b == 0x0E:  # word
                cmd += str(struct.unpack("<H", data[i:i+2])[0]).encode('ascii')
                i += 2
            elif b == 0x0F:  # byte
                cmd += str(data[i]).encode('ascii')
                i += 1
            elif b == 0x1C:  # word ??
                # todo: how it's different from 0x0E?
                cmd += str(struct.unpack("<H", data[i:i+2])[0]).encode('ascii')
                i += 2
            elif b >= ord('A') and b <= ord('z') and data[i] >=0 and data[i] <= 0x20:  # variable?
                cmd += bytes([b])
                varlen = data[i]
                if varlen > 0:
                    cmd += struct.unpack("{}s".format(varlen), data[i+1:i+varlen+1])[0]
                i += varlen + 1
            elif b == ord('"'):  # string
                cmd += b'"'
                while data[i] != ord('"'):
                    cmd += bytes([data[i]])
                    i += 1
                cmd += b'"'
                i += 1
            elif chr(b) in (':', ';', ',', '*', '#', '$', '%', '(', ')'):
                if data[i] != 0x99:  # todo: why is that?
                    cmd += bytes([b])
            elif b == 0x82: cmd += b"BLOAD"
            elif b == 0x84: cmd += b"CONSOLE"
            elif b == 0x86: cmd += b"CLOSE"
            elif b == 0x88: cmd += b"CLEAR"
            elif b == 0x89: cmd += b"CALL"
            elif b == 0x8E: cmd += b"COLOR"
            elif b == 0x8F: cmd += b"CLS"
            elif b == 0x91:
                cmd += b"DATA"
                cmd += data[i:-1]
                break
            elif b == 0x92: cmd += b"DIM"
            elif b == 0x94: cmd += b"DEFINT"
            elif b == 0x98: cmd += b"DEF"
            elif b == 0x99: cmd += b"ELSE"
            elif b == 0x9B: cmd += b"ERASE"
            elif b == 0x9D: cmd += b"ERROR"
            elif b == 0x9E: cmd += b"FOR"
            elif b == 0x9F: cmd += b"FIELD"
            elif b == 0xA3: cmd += b"GOTO"
            elif b == 0xA4: cmd += b"GOSUB"
            elif b == 0xA5: cmd += b"GET"
            elif b == 0xA7: cmd += b"INPUT"
            elif b == 0xA8: cmd += b"IF"
            elif b == 0xAC: cmd += b"LOCATE"
            elif b == 0xB0: cmd += b"LINE"
            elif b == 0xB7: cmd += b"NEXT"
            elif b == 0xBB: cmd += b"OPEN"
            elif b == 0xBC: cmd += b"OUT"
            elif b == 0xBD: cmd += b"ON"
            elif b == 0xBF: cmd += b"OFF"
            elif b == 0xC0: cmd += b"PRINT"
            elif b == 0xC2: cmd += b"POKE"
            elif b == 0xC5: cmd += b"PAINT"
            elif b == 0xC6: cmd += b"RETURN"
            elif b == 0xC7: cmd += b"READ"
            elif b == 0xC8: cmd += b"RUN"
            elif b == 0xC9: cmd += b"RESTORE"
            elif b == 0xCB: cmd += b"RESUME"
            elif b == 0xCE: cmd += b"RANDOMIZE"
            elif b == 0xD0: cmd += b"SCREEN"
            elif b == 0xD1: cmd += b"STOP"
            elif b == 0xD2: cmd += b"SWAP"
            elif b == 0xD4: cmd += b"SPC"
            elif b == 0xD5: cmd += b"STEP"
            elif b == 0xD6: cmd += b"THEN"
            elif b == 0xDA: cmd += b"TO"
            elif b == 0xDE: cmd += b"WIDTH"
            elif b == 0xDF: cmd += b"WAIT"
            elif b == 0xE0: cmd += b"WHILE"
            elif b == 0xE1: cmd += b"WEND"
            elif b == 0xE2: cmd += b"WRITE"
            elif b == 0xE4: cmd += b"SEG"
            elif b == 0xF0: cmd += b">"
            elif b == 0xF1: cmd += b"="
            elif b == 0xF2: cmd += b"<"
            elif b == 0xF3: cmd += b"+"
            elif b == 0xF4: cmd += b"-"
            elif b == 0xF5: cmd += b"*"
            elif b == 0xF6: cmd += b"/"
            elif b == 0xF8: cmd += b"AND"
            elif b == 0xF9: cmd += b"OR"
            elif b == 0xFD: cmd += b"MOD"
            elif b == 0xFE: cmd += b"\\"
            elif b == 0xFF:  # function
                b = data[i]
                i += 1
                if b == 0x81: cmd += b"MID$"
                elif b == 0x84: cmd += b"TIME$"
                elif b == 0x92: cmd += b"ASC"
                elif b == 0x98: cmd += b"CVI"
                elif b == 0x9C: cmd += b"CHR$"
                elif b == 0x9E: cmd += b"ERL"
                elif b == 0x9F: cmd += b"ERR"
                elif b == 0xA4: cmd += b"HEX$"
                elif b == 0xA6: cmd += b"INT"
                elif b == 0xA8: cmd += b"INKEY$"
                elif b == 0xAC: cmd += b"LEN"
                elif b == 0xAD: cmd += b"LEFT$"
                elif b == 0xAF: cmd += b"MKI$"
                elif b == 0xB5: cmd += b"PEEK"
                elif b == 0xB6: cmd += b"RIGHT$"
                elif b == 0xB7: cmd += b"RND"
                elif b == 0xBC: cmd += b"STR$"
                elif b == 0xC0: cmd += b"VAL"
                elif b == 0xC2: cmd += b"FRE"
                elif b == 0xC3: cmd += b"VARPTR"
                elif b == 0xCC: cmd += b"AKCNV$"
                elif b == 0xCF: cmd += b"STATUS"
                else: print("line {}: unknown function {:X}".format(line_num, b))
            else:
                print("line {}: unknown opcode {:X}".format(line_num, b))
        line = str(line_num).encode('ascii')
        if cmd[0] != 0x20: line += b' '
        line += cmd
        txt += line + b'\x0d\x0a'
        if False:
            if cmd != '':
                print(line)
            else:
                print(length, line_num, data)
    return txt


if __name__ == '__main__':
    with open(sys.argv[1], 'rb') as f:
        decompile(f.read())