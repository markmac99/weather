# dummy module to emulate reading data from the USB weatherstation
"""
    example data block
    0000 55 aa ff ff ff ff ff ff ff ff ff ff ff ff ff ff 05 20 01 41 11 00 00 00 81 00 00 0f 05 00 e0 51
    0020 03 27 ce 27 00 00 00 00 00 00 00 12 02 14 18 27 41 23 c8 00 00 00 46 2d 2c 01 64 80 c8 00 00 00
    0040 64 00 64 80 a0 28 80 25 a0 28 80 25 03 36 00 05 6b 00 00 0a 00 f4 01 12 00 00 00 00 00 00 00 00
    0060 00 00 49 0a 63 12 05 01 7f 00 36 01 60 80 36 01 60 80 bc 00 7b 80 95 28 12 26 6c 28 25 26 c8 01
    0080 1d 02 d8 00 de 00 ff 00 ff 00 ff 00 00 11 10 06 01 29 12 02 01 19 32 11 09 09 05 18 12 01 22 13
    00a0 14 11 11 04 15 04 11 12 17 05 12 11 09 02 15 26 12 02 11 07 05 11 09 02 15 26 12 02 11 07 05 11
    00c0 09 10 09 12 12 02 02 12 38 12 02 07 19 00 11 12 16 03 27 12 02 03 11 00 11 12 16 03 27 11 12 26
    00e0 21 32 11 12 26 21 32 12 02 06 19 57 12 02 06 19 57 12 02 06 19 57 12 02 06 19 57 12 02 06 19 57

"""
"""
The weatherstation stores its current data in a 256-byte buffer as shown above. 

The Weatherstation() class in pywws creates an instance of CUSBDrive() which contains an instance of USBDevice(). 

CUSBDrive() has two methods:
read_block(self, address) which instructs USBDevice to advance to "address" in its buffer then read 32  or 8 bytes 
write_byte(self, address, byte) which instructs USBDevice to overwrite the byte at address.

The original weatherstation has two chunks of memory. A 256-byte "fixed block" and a 65280 byte ring buffer containing the 16-byte current data.
The fixed block contains the address of the current data within the ring buffer. 
So, to read the w/s you need to first read the fixed buf to get the offset, then read the ring buffer.
We can dummy this out by treating offset of zero as reading the fixed buffer, and any other value as being a pointer to teh real data.

pywws/weatherstation.py expects a few values to be in the fixed block:
    0,1: magic bytes, must be 0x55, 0xAA to indicate its valid data
    16: read_period - how often to read the data, min 48 seconds
    26: data_changed - 0xAA to indicate it has changed
    27-28: data_count - two byte int, counter incrementing from zero at reboot, updating each time new data written to buffer
    32-33: current_pos - current offset to the "real" data, eg 0x0120 in the above example
    Other data in this block seems unused and can be zero

Active station data must be at address 0x0100 and beyond, and is as follows
    delay, hum_in, temp_in (signed 2bytes), hum_out, temp_out (signed 2b), abs_press (2b), wind_ave (1.5 bytes), wind_gust (1.5 b), wind_dir, rain (2b), status
    the two wind values share bytes 9,10,11 with the low four bits of 11 belonging to 9
    delay must be nonzero and less than 35
CUSBDevice() has two methods as shown below.
"""


def createSomeData():
    delay = 1
    hum_in = 45
    temp_in = 19.3
    tin_lo = int((temp_in / 0.1) % 256)
    tin_hi = int((temp_in / 0.1) // 256)
    hum_out = 67
    temp_out = -4.5 / 0.1

    tout_lo = int((temp_out / 0.1) % 256)
    tout_hi = int((temp_out / 0.1) // 256)
    abs_press = 1020
    apress_lo = int((abs_press / 0.1) % 256)
    apress_hi = int((abs_press / 0.1) // 256)
    wind_ave = 1.5
    wave_bv = wind_ave / 0.1
    wind_gust = 2.4
    wgus_bv = wind_gust / 0.1
    shr_bv = 0 
    wind_dir = 5
    rain = 12.5
    rain_lo = int((rain / 0.3) % 256)
    rain_hi = int((rain / 0.3) // 256)
    status = 0
    return [delay, hum_in, tin_lo, tin_hi, hum_out, tout_lo, tout_hi, apress_lo, apress_hi, wave_bv, wgus_bv, shr_bv, wind_dir, rain_lo, rain_hi, status]


class USBDevice(object):
    EndMark = 0x20
    ReadCommand = 0xA1
    WriteCommand = 0xA0
    WriteCommandWord = 0xA2
    SuccessMarker = 0xA5

    def __init__(self, idVendor, idProduct):
        self.data = [0x55, 0xaa, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
                     0x05, 0x20, 0x01, 0x41, 0x11, 0x00, 0x00, 0x00, 0x81, 0x7f, 0x00, 0xf0, 0x0f, 0x00, 0x50, 0x04,
                     0x64, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,]
        self.offset = 0
        return 

    def read_data(self, size):
        # if size is 32 read 32 bytes from the current offset.
        # if size is 8, return 0xA5 to indicate a successful write took place.
        if size == 0x20:
            # the fixed block is the first 256 bytes but we only need the first 64 
            if self.offset > 0x20 and self.offset < 0x0100:
                result = [0] * size 
            elif self.offset >= 0x0100:
                print('reading some actual data')
                result = [0] * size 
            else:
                result = self.data[self.offset:self.offset+size]
        else:
            result = [self.SuccessMarker]
        return list(result)

    def write_data(self, buf):
        if buf[0] == self.ReadCommand:
            self.offset = buf[2] + buf[1] * 256
        elif buf[0] == self.WriteCommandWord:
            addr = buf[2] + buf[1] * 256
            val = buf[5]
            self.data[addr] = val
        else:
            print('unknown command')
        return True


def main(class_, argv=None):
    return
