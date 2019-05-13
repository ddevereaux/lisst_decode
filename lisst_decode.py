import math, struct
import os, mmap

datagram_size = 12

field_names = ('time1', 'time2', 'vol_conc', 'part_size', \
          'opt_trans', 'laser_ref')

class Lisst(object):
    def __init__(self, filename, use_mmap=True):

        sbet_file = open(filename)

        if use_mmap:
            sbet_size = os.path.getsize(filename)
            self.data = mmap.mmap(sbet_file.fileno(), sbet_size, access=mmap.ACCESS_READ)
        else:
            self.data = sbet_file.read()

        # Make sure the file is sane
        assert(len(self.data)%datagram_size == 0)

        self.num_datagrams = len(self.data) / datagram_size

    def decode(self, offset=0):
        'Return a dictionary for an SBet datagram starting at offset'

        subset = self.data[ offset : offset+ datagram_size ]
        values = struct.unpack('6h', subset)

        lisst_values = dict(zip (field_names, values))

        #lisst_values['lat_deg'] = math.degrees(sbet_values['latitude'])
        #sbet_values['lon_deg'] = math.degrees(sbet_values['longitude'])

        return lisst_values

    def get_offset(self, datagram_index):
        return datagram_index * datagram_size

    def get_datagram(self, datagram_index):
        offset = self.get_offset(datagram_index)
        values = self.decode(offset)
        return values

    def __iter__(self):
        return LisstIterator(self)

class LisstIterator(object):
    'Independent iterator class for Sbet files'
    def __init__(self,lisst):
        self.lisst = lisst
        self.iter_position = 0

    def __iter__(self):
        return self

    def next(self):
        if self.iter_position >= self.lisst.num_datagrams:
            raise StopIteration

        values = self.lisst.get_datagram(self.iter_position)
        self.iter_position += 1
        return values

def main():
   # print 'Datagram Number, Time, x, y'

    lisst = Lisst('li0002b')
    for index, datagram in enumerate( Lisst('li0002b') ):
        print index, datagram['time1'], datagram['vol_conc'], datagram['part_size'], \
        datagram ['opt_trans'], datagram ['laser_ref']

if __name__ == '__main__':
    main()

