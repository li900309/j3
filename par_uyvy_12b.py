#!/usr/bin/python3


from ctypes import *
from curses import raw
import struct

class UYVY_RAW_12b(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('Y0',  c_uint, 12),
        ('U', c_uint, 12),
#        ('Y1',  c_uint, 8),
#        ('V', c_uint, 12),
    ]


class UY_RAW_12b(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('Y',  c_uint, 12),
        ('U', c_uint, 12),
        ('res', c_uint, 8),
    ]
class VY_RAW_12b(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('res', c_uint, 8),
        ('V', c_uint, 12),
        ('Y', c_uint, 12),
    ]

raw_data = open("./yuv422.bin", "rb").read()
print(len(raw_data))

y8_file = open("y8.raw", "w+b")
y8_file.seek(0)

H = 720
W = 1280

#for i in range(len(raw_data)):
#    print("%02x " % raw_data[i], end="")
#    if ((i % 27) == 0):
#        print("")

pos = 0
raw_y8 = []
while (pos < len(raw_data)):
    uy_pix = UY_RAW_12b()
    vy_pix = VY_RAW_12b()

    tmp_data = raw_data[pos:pos+7]
#    for d in tmp_data:
#        print("%02x" % d)
    t1 = raw_data[pos:pos+4]
    t2 = raw_data[pos+2:pos+6]
    for x in t2:
        print("%02x" % x)
    memmove(addressof(uy_pix), t1, sizeof(uy_pix))
    memmove(addressof(vy_pix), t2, sizeof(vy_pix))

    U = (uy_pix.U)
    Y0 = (uy_pix.Y)
    V = (vy_pix.V)
    Y1 = (vy_pix.Y)

    y8_file.write(struct.pack('B', Y0 >> 4))
    y8_file.write(struct.pack('B', U >> 4))
    y8_file.write(struct.pack('B', Y1 >> 4))
    y8_file.write(struct.pack('B', V >> 4))
    #print("%02x" % (Y))
    pos += 6

y8_file.close()
