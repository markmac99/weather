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
    print(data)
