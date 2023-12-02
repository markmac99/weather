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
import json
import os
import time


def createSomeData(whfname, ):
    if not os.path.isfile(whfname):
        print('unable to open weather data files')
        return [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    lis = open(whfname,'r').readlines()
    try:
        lastline = lis[-1].strip()
        eles = json.loads(lastline)
    except Exception:
        print('malformed line')
        return [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    temp_out = eles['temperature_C']
    hum_out = eles['humidity']
    wind_ave = eles['wind_avg_km_h']
    wind_gust = eles['wind_max_km_h']
    wind_dir = int(int(eles['wind_dir_deg'])/45)
    rain = eles['rain_mm']
    temp_in = eles['temp_c_in']
    abs_press = eles['press_rel']
    hum_in = eles['humidity_in']
                     
    delay = 1
    hum_in = int(hum_in)
    hum_out = int(hum_out)
    tin_lo = int((temp_in / 0.1) % 256)
    tin_hi = int((temp_in / 0.1) // 256)
    tout_lo = int((temp_out / 0.1) % 256)
    tout_hi = int((temp_out / 0.1) // 256)
    apress_lo = int((abs_press / 0.1) % 256)
    apress_hi = int((abs_press / 0.1) // 256)
    wave_bv = int((wind_ave / 0.1) % 256)
    wgus_bv = int((wind_gust / 0.1) % 256)
    shr_bv = int((wind_ave / 0.1) // 256) + (int((wind_gust / 0.1) // 256) << 4)
    rain_lo = int((rain / 0.3) % 256)
    rain_hi = int((rain / 0.3) // 256)
    status = 0
    time.sleep(2)
    return [delay, hum_in, tin_lo, tin_hi, hum_out, tout_lo, tout_hi, 
            apress_lo, apress_hi, wave_bv, wgus_bv, shr_bv, wind_dir, rain_lo, rain_hi, status]


class USBDevice(object):
    EndMark = 0x20
    ReadCommand = 0xA1
    WriteCommand = 0xA0
    WriteCommandWord = 0xA2
    SuccessMarker = 0xA5

    def __init__(self, idVendor, idProduct):
        self.data = [0x55, 0xaa, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
                     0x01, 0x20, 0x01, 0x41, 0x11, 0x00, 0x00, 0x00, 0x81, 0x7f, 0x00, 0xf0, 0x0f, 0x00, 0x50, 0x04,
                     0x64, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,]
        self.current_pos = 0
        self.whfname = '/home/pi/weather/weatherdata.json'

        return 

    def read_data(self, size):
        # if size is 32 read 32 bytes from the current offset.
        # if size is 8, return 0xA5 to indicate a successful write took place.
        if size == 0x20:
            # the fixed block is the first 256 bytes but we only need the first 64 
            if self.current_pos < 0x40:
                result = self.data[self.current_pos:self.current_pos + size]
            elif self.current_pos >= 0x40 and self.current_pos < 0x0100:
                result = [0] * size 
            else:
                self.current_pos += 0x20
                if self.current_pos > 0x1000:
                    self.current_pos = 0x0100
                self.data[30] = self.current_pos % 256
                self.data[31] = self.current_pos // 256
                result = createSomeData(self.whfname) + [0] * 16
        else:
            result = [self.SuccessMarker]
        return list(result)

    def write_data(self, buf):
        if buf[0] == self.ReadCommand:
            self.current_pos = buf[2] + buf[1] * 256
            #self.data[30] = buf[2]
            #self.data[31] = buf[1]
        elif buf[0] == self.WriteCommandWord:
            addr = buf[2] + buf[1] * 256
            if addr == 26:
                # in a real WH1080 would write 0xAA to indicate data changed but we dont want that
                self.data[addr] = 0x00
            else:
                val = buf[5]
                self.data[addr] = val
        else:
            print('unknown command')
        return True


def main(class_, argv=None):
    return
