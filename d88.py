from struct import unpack, calcsize, Struct
import sys
import array

# D88 header:
# 	char title[17];
#   BYTE rsrv[9];
#	BYTE protect;
#	BYTE type;
#	DWORD size;
#	DWORD trkptr[164] - can't decode directly, put in another structure;
d88_header_fmt = '<17s9sBB1i'
d88_header_len = calcsize(d88_header_fmt)
d88_header_unpack = Struct(d88_header_fmt).unpack_from

# D88 track header:
#	BYTE c, h, r, sector_size;
#	WORD nsec;
#	BYTE density, del, stat;
#	BYTE rsrv[5];
#	WORD size;
sector_header_fmt = '<BBBBHBBB5sH'
sector_header_len = calcsize(sector_header_fmt)
sector_header_unpack = Struct(sector_header_fmt).unpack_from

DENSITY_DOUBLE = 0
DENSITY_HIGH = 1
DENSITY_SINGLE = 64


class D88IMAGE:
    tracks_dir = ()  # (side 0 = [cylinder...]={sector...}, side 1 = [cylinder...]={sector...})

    def __init__(self, sides=2, density=DENSITY_HIGH, sectors=26,sector_size=256):
        self.tracks_dir = ([], [])
        # todo: init new diskette image
        pass

    def sector_size_to_bytes(self, sector_size):
        return 0x80 << sector_size

    def density_to_string(self, density):
        if density == DENSITY_DOUBLE:
            return "double"
        elif density == DENSITY_HIGH:
            return "high"
        elif density == DENSITY_SINGLE:
            return "single"
        else:
            raise ("Unknown density " + density + ", could be single?")

    def load(self, filename):
        with open(filename, 'rb') as f:
            raw = f.read(d88_header_len)
            d88_header = d88_header_unpack(raw)
            (title, rsrv, protect, type, size) = d88_header
            # tracks = array.array('I')
            # tracks.read(f, 164) # trkptr structure
            # tracks = tracks.tolist()
            tracks = unpack("164I", f.read(164 * 4))
            print('Filename:', filename)
            print('Title:', title.decode())
            # print 'Tracks:', tracks
            actual_tracks = list(filter(lambda x: x > 0, tracks))
            print('Tracks actually in use:', len(actual_tracks))

            self.tracks_dir = ([], [])
            for track_origin in actual_tracks:
                f.seek(track_origin)
                raw = f.read(sector_header_len)
                track_header = sector_header_unpack(raw)
                (c, h, r, sector_size, nsec, density, _del, stat, rsrv, size) = track_header
                f.seek(track_origin)
                cur_head = h
                self.tracks_dir[h].append({})
                for sec_id in range(nsec):
                    track_header = sector_header_unpack(f.read(sector_header_len))
                    (c, h, r, sector_size, nsec, density, _del, stat, rsrv, size) = track_header
                    #print('Cylinder', c, 'Head', h, 'Sector', r, end=' ')
                    #print('Sector size (in bytes):', self.sector_size_to_bytes(sector_size), end=' ')
                    #print('Density:', self.density_to_string(density))
                    if self.sector_size_to_bytes(sector_size) != size:
                        raise Exception("Malformated sector size")
                    if cur_head != h:
                        raise Exception("Head out of order")
                    self.tracks_dir[h][c][r] = f.read(size)


def usage():
    print(sys.argv[0] + " [d88 file]")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage()
        sys.exit(1)

    image = D88IMAGE()
    image.load(sys.argv[0])
