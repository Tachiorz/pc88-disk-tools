import os
import sys
from collections import namedtuple
import struct
import n88basic
from d88 import D88IMAGE

DEBUG = False

def usage():
    print("Extract files from N88 BASIC disk")
    print(sys.argv[0] + " [d88 file]")


def file_attribute_to_string(attr):
    if attr == 0:
        return "ASCII"
    elif attr == 1:
        return "Machine language"
    elif attr == 0x10:
        return "ASCII, write protected"
    elif attr == 0x40:
        return "ASCII, read after write"
    elif attr == 0x80:
        return "non-ASCII"
    elif attr == 0x90:
        return "non-ASCII, write protected"
    elif attr == 0xa0:
        return "non-ASCII, encrypted"
    elif attr == 0xc0:
        return "non-ASCII, read after write"


def cluster_to_head_track(cluster):
    head = cluster & 1
    track = cluster >> 1
    return head, track


if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage()
        sys.exit(1)

    decompile = True

    image = D88IMAGE()
    image.load(sys.argv[1])

    # Disk ID. Cylinder 35 Sector 23
    class DiskId:
        __slots__ = 'attribute', 'number_of_files', 'basic_code'
    disk_id = DiskId()
    disk_id.attribute, disk_id.number_of_files, disk_id.basic_code = \
        struct.unpack('<BB254s', image.tracks_dir[0][35][23])
    disk_id.basic_code = bytes(disk_id.basic_code).strip(b'\x00')
    print('Startup code:', disk_id.basic_code)

    # Directory. Cylinder 35 Sector 24-26
    class DirectoryItem:
        __slots__ = 'filename', 'fileext', 'attribute', 'first_cluster'
    directory = []
    print('Files:')
    for sector in range(1, 22):
        for i in range(16):
            di = DirectoryItem()
            di.filename, di.fileext, di.attribute, di.first_cluster, _ = \
                struct.unpack('<6s3sBB5s', image.tracks_dir[0][35][sector][i*16: i*16 + 16])
            if di.attribute == 0xff: continue
            di.filename = di.filename.decode("shift-jis").strip()
            di.fileext = di.fileext.decode("shift-jis").strip()
            directory.append(di)

    # FAT. Cylinder 35 Sector 24-26
    # FAT[0:0x99] continuous cluster, value indicates the number of the subsequent cluster
    # FAT[0xC1:0xDA] last cluster, lower 5 bits indicate the number of sectors actually used in the cluster
    # Values:
    # 0xFF: empty cluster
    # 0xFE: cluster can't be used
    output_dir = sys.argv[1] + '_DUMP\\'
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    FAT = image.tracks_dir[0][35][24] + image.tracks_dir[0][35][25] + image.tracks_dir[0][35][26]
    for di in directory:
        filename = di.filename
        if di.fileext != '': filename += '.' + di.fileext
        print(filename, file_attribute_to_string(di.attribute))
        cluster = di.first_cluster
        with open(output_dir + filename, 'wb') as f:
            buf = b''
            while True:
                if DEBUG: print(cluster, end=",")

                last_cluster = FAT[cluster] >= 0xC1 and FAT[cluster] < 0xDA

                head, track = cluster_to_head_track(cluster)
                if last_cluster:
                    sector_count = FAT[cluster] & 0x1F
                    if DEBUG: print("sectors:", sector_count)
                else:
                    sector_count = len(image.tracks_dir[head][track])
                for s in range(1, sector_count + 1):
                    buf += image.tracks_dir[head][track][s]
                if last_cluster:
                    break
                cluster = FAT[cluster]
            if decompile:
                decompile_dir = output_dir + 'decompile\\'
                if not os.path.exists(decompile_dir):
                    os.mkdir(decompile_dir)
                try:
                    dec = n88basic.detokenize(buf)
                    out = n88basic.n88basic_to_utf8(dec)
                    with open(decompile_dir + filename, 'wb') as fd:
                        fd.write(out)
                except Exception as e:
                    print(e)
            f.write(buf)

