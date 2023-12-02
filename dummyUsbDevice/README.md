# README for dummy USB driver for pywws


Pywws uses a simple USB interface to read data from the WH1080/3080 Fine Offset weatherstations. These
devices, once sold by Maplin, provide all the usual weather related data. 

## How the Station stores data
The weatherstation has a 64KB buffer. The first 256 bytes are a "fixed block" containing data such as configuration, data read frequency, max/min values, etc. The remaining 65280 bytes form a ring buffer.
Each time it takes a reading, the weatherstation writes the data to  the next 32-byte slot in the ring buffer, and then the address of this slot is written to the two bytes at fixed block 0x0020. So for example if the address 0x0140 then current_pos in fixed_block will contain this value. Meanwhile bytes 27/28 contain an integer data_count that is incremented from zero after each write. The period of data generation is set by byte 16 of the fixed block, and is an integer with a minimum value of 48. This corresponds to a one-minute frequency, as the system always waits 12s before reading data. 
The WH1080 has 16-byte datablocks, whereas the WH3080 has 20-byte blocks. 

## How pywws collects data
The software uses the current_pos and data_count to decide whether to read data. Upon startup, it reads the data_count and stores it in memory. Each time it requests new data, the data_count is checked to make sure it has incremented, and then the data are read from the current_pos address. If the data_count hasn't incremented then the system backs off for a random time interval and retries. 

## How pywws actually reads the data
The Weatherstation() class in pywws creates an instance of CUSBDrive() which contains an instance of USBDevice(). I know... Anyway... 

### CUSBDrive() 
This has two methods 
* read_block(self, address) which instructs USBDevice to read 32 bytes starting at "address".  
* write_byte(self, address, byte) which instructs USBDevice to overwrite the byte at "address". 

### USBDevice()
This has two methods:
* read_data(self, size) which reads 'size' bytes from wherever the current_pos pointer is pointing. Returns the data if sucessful. 
* write_data(self, buf) which writes data from buf to the address specified in buf. Returns 0xA5 if successful. 

The 'buf' structure contains eight bytes. If the first byte is OXA1 then the next two bytes are the address to select. No data is written. If the first byte is OxA2, then the next two bytes contain the address and the sixth  contains the value to write. Addresses and values are in low byte, high byte order.

## How I am dummying it out
I've created a dummy USBDevice() which implements the same methods. The read method will then retrieve weather data from MQ or file, and return it to pywws in the required format. 

The dummy driver to handle all the cases that the real driver implements: 
* read raw data from any address in the current block. 
* write 0xAA to fixed_block 26 to indicate that data has changed, then set it back to zero.
* read the entire fixed_block into memory by calling read_data(32) eight times.
* increment current_pos by 0x20 every time a new reading is available
* Other stuff TBC


## Some details of the fixed block and ring buffer
Full details are in weatherstation.py

pywws/weatherstation.py expects a few values to be in the fixed block:
* 0,1: magic bytes, must be 0x55, 0xAA to indicate its valid data
* 16: read_period - how often to read the data, min 48 seconds
* 26: data_changed - 0xAA to indicate it has changed, then set back to zero immediately
* 27-28: data_count - two byte int, counter incrementing from zero at reboot, updating each time new data written to buffer
* 32-33: current_pos - current offset to the "real" data, eg 0x0120 in the above example

Other data in this block seems unused and can be zero

Active station data must be at address 0x0100 and beyond, and is as follows
*delay, hum_in, temp_in (signed 2bytes), hum_out, temp_out (signed 2b), abs_press (2b), wind_ave (1.5 bytes), wind_gust (1.5 b), wind_dir, rain (2b), status
* the two wind values share bytes 9,10,11 with the low four bits of 11 belonging to 9
* delay must be nonzero and less than 35

The signed floats and wind data are stored in a complex fashion. More details to come


USBDevice().read_block(address)
if address < 256
	return fixed_blcck[address:address+32]
else
	increment fixed_block[data_count]
	return the current set of weather data
		this should load some data from wherever and return within 12 secs

USBDevice().write_data(buf):
if buf[0] is ReadCommand
	set fixed_block[current_pos] to the address values
if buf[0] is WriteCommandWord
	if address > 255, error ! 
	set fixed_block[address] to buf[5] unless address is 25 (data_changed)
else
	error
	

Separately, 
on startup initialise fixed_block[0:256] to all-zeros except for 
	fixed_block[0] = 0x55
	fixed_block[1] = 0xAA
	fixed_block[16] = read_period in seconds
	

