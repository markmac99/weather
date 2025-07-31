from weatherstation import WSInt, WSFloat, WSStatus

# test the dummy usb module
if __name__ =='__main__':
    EndMark = 0x20
    ReadCommand = 0xA1
    WriteCommand = 0xA0
    WriteCommandWord = 0xA2
    SuccessMarker = 0xA5

    module_name = 'dummyUsbReader'
    module = __import__(module_name)
    myUSBDevice = getattr(module, 'USBDevice')
    dev = myUSBDevice(0x1941, 0x8021)

    data = dev.read_data(32)
    print(data)

    address = 0x20
    buf = [ReadCommand, address // 256, address % 256, EndMark, ReadCommand, address // 256, address % 256, EndMark,]    
    res = dev.write_data(buf)
    data = dev.read_data(32)
    print(data)

    address = 0x40
    buf = [ReadCommand, address // 256, address % 256, EndMark, ReadCommand, address // 256, address % 256, EndMark,]    
    res = dev.write_data(buf)
    data = dev.read_data(32)
    print(data)

    address = 0x0200
    buf = [ReadCommand, address // 256, address % 256, EndMark, ReadCommand, address // 256, address % 256, EndMark,]    
    res = dev.write_data(buf)
    data = dev.read_data(32)

    delay = WSInt.from_1(data,0)
    hum_in = WSInt.from_1(data,1)
    temp_in = WSFloat.from_2(data, 2, signed=True, scale=0.1)
    hum_out = WSInt.from_1(data,4)
    temp_out = WSFloat.from_2(data, 5, signed=True, scale=0.1)
    abs_pres = WSFloat.from_2(data, 7, signed=True, scale=0.1)
    wind_ave = WSFloat.from_1(data,9, scale=0.1, nibble_pos=11, nibble_high=False)
    wind_gus = WSFloat.from_1(data,10, scale=0.1, nibble_pos=11, nibble_high=True)
    wind_dir = WSInt.wind_dir(data,12)
    rain = WSFloat.from_2(data, 13, signed=False, scale=0.3)
    status = WSStatus.from_raw(data,15)

    print(f'hum_in {hum_in}, temp_in {temp_in}')
    print(f'hum_out {hum_out}, temp_out {temp_out}')
    print(f'abs_press {abs_pres} rain {rain}')
    print(f'wind_ave {wind_ave} wind_gust {wind_gus} wind_dir {wind_dir}')
    print(f'delay {delay} status {status}')
