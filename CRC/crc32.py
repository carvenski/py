"""
Library for calculating CRC3/CRC4/CRC8/CRC16/CRC24/CRC32/CRC64/CRC82.
使用CRC哈希函数生成特定位数的数字.
"""
import libscrc

crc32 = libscrc.crc32(b'test') 
print(crc32)

crc64 = libscrc.iso(b'test')
print(crc64)

