import sys
from d88 import D88IMAGE


def usage():
    print("Convert N88 BASIC formatted D88 disks to 256 byte per sector RAW images")
    print(sys.argv[0] + " [d88 file]")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage()
        sys.exit(1)

    image = D88IMAGE()
    image.load(sys.argv[1])
    if len(image.tracks_dir[0][0][1]) == 128 and len(image.tracks_dir[0][0]) == 26:
        print("Looks like N88 basic image")
        print("Converting to HD 2 Side 77 cyl 26 sec of 256 bytes")
        wf = open(sys.argv[1] + '.HDB.img', 'wb')
        for i in range(1, 27):  # convert bootloader
            wf.write(image.tracks_dir[0][0][i])
        wf.write(b'\x40' * 128 * 26)
        for s in range(1, 27):
            wf.write(image.tracks_dir[1][0][s])
        for i in range(1, 77):
            for h in range(2):
                for s in range(1,27):
                    data = image.tracks_dir[h][i][s]
                    if len(data) != 256: raise Exception("wrong sector length")
                    wf.write(data)
        wf.close()
