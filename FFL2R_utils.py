from FFL2R_data import GameData

EIGHT_BIT_INT = 255
SIXTEEN_BIT_INT = 65535

class Utility:
    twoBytes = lambda x, y : y << EIGHT_BIT_INT.bit_length() | x
    threeBytes = lambda x, y, z : z << SIXTEEN_BIT_INT.bit_length() | y << EIGHT_BIT_INT.bit_length() | x
    byteizeTwo = lambda x : (x & EIGHT_BIT_INT, x >> EIGHT_BIT_INT.bit_length() & EIGHT_BIT_INT)
    byteizeThree = lambda x : (x & EIGHT_BIT_INT, x >> EIGHT_BIT_INT.bit_length() & EIGHT_BIT_INT, x >> SIXTEEN_BIT_INT.bit_length() & SIXTEEN_BIT_INT)
    findCoordinate = lambda byte : ((byte & 0x3f) | (((byte & 0x3f) >> 4) << 4))
    remainingBytes = lambda byte, sub : ((byte - sub) & 0xf0) >> 6
    highNibble = lambda byte : (byte & 0xf0) >> 4
    lowNibble = lambda byte : byte & 0x0f
    isbitset = lambda byte, bit: bool((byte >> bit) & 1)

    def setBoundaries(num:int, floor:int, ceiling:int) -> int:
        if num < floor:
            num = floor
        elif num > ceiling:
           num = ceiling
        return num

    def dteTranslate(strList:bytearray)->str:
        result = ""
        for char in strList:
            try:
                result = result + (GameData.dteLookup[char])
            except:
                result = result + " " + (str(char))
        return result

    def listToHex(intList:list)->list:
        return [hex(x) for x in intList]