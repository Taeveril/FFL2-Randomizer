import mmap
from FFL2R_utils import Utility

class ScriptManager:
    def __init__(self, rom:mmap):
        self.SCRIPT_BLOCK_1 = (0x2c000, 0x2eb7f, 0x28000, 0)
        self.SCRIPT_BLOCK_2 = (0x28000, 0x2be3e, 0x24000, 256)
        self.BATTLE_BLOCK = (0x2eb80, 0x2f3ff, 0x28000, 0)
        self.MENU_BLOCK = (0x2f400, 0x2ffcf, 0x28000, 0)
        self.MEMO_BLOCK = (0x3c270, 0x3e037, 0x38000, 0, 0x3c46f)
        self.main = self._populateBlock(rom, self.SCRIPT_BLOCK_1[0], self.SCRIPT_BLOCK_1[1], self.SCRIPT_BLOCK_1[2], self.SCRIPT_BLOCK_1[3]) | self._populateBlock(rom, 
                    self.SCRIPT_BLOCK_2[0], self.SCRIPT_BLOCK_2[1], self.SCRIPT_BLOCK_2[2], self.SCRIPT_BLOCK_2[3])
        self.battle = self._populateBlock(rom, self.BATTLE_BLOCK[0], self.BATTLE_BLOCK[1], self.BATTLE_BLOCK[2], self.BATTLE_BLOCK[3])
        self.menu = self._populateBlock(rom, self.MENU_BLOCK[0], self.MENU_BLOCK[1], self.MENU_BLOCK[2], self.MENU_BLOCK[3])
        self.memo = self._populateBlock(rom, self.MEMO_BLOCK[0], self.MEMO_BLOCK[1], self.MEMO_BLOCK[2], self.MEMO_BLOCK[3], self.MEMO_BLOCK[4])
        self.banks = (self.main, self.battle, self.menu, self.memo)

    def _populateBlock(self, rom:mmap, startAddr:int, endAddr:int, offset:int, indexer:int, *memoAddr)->dict:
        d = {}
        if memoAddr:
            relHeaderEnd = memoAddr[0] - startAddr + 1
        else:
            relHeaderEnd = Utility.twoBytes(rom[startAddr], rom[startAddr+1]) - (startAddr - offset)
        for i in range(0, relHeaderEnd, 2):
            script = bytearray()
            relAddr = Utility.twoBytes(rom[startAddr+i], rom[startAddr+i+1])
            if i != relHeaderEnd-2:
                length = Utility.twoBytes(rom[startAddr+i+2], rom[startAddr+i+3]) - relAddr
            else: #last entry, go back from end and hunt down non-0x00 data
                if Utility.twoBytes(rom[startAddr+i], rom[startAddr+i+1]) + offset != endAddr:
                    j = endAddr
                    while rom[j] == 0x00:
                        j-=1
                    length = (j - offset) - relAddr + 2
                else: #at the end of the block! no more bytes!
                    length = 1
            for x in range(0, length):
                script.append(rom[offset+relAddr+x])
            d[int(i/2) + indexer] = script
        return d

    def addNewScript(self, bank:int, data:str):
        def _findNextIndex(start:int, stop:int, targetDict:dict)->int|None:
            for targetIndex in range(start, stop):
                if targetIndex not in targetDict.keys():
                    return targetIndex
        def _tryToAdd(targetDict:dict, targetIndex:int|None):
            if targetIndex:
                targetDict[targetIndex] = data
            else:
                print(f"Could not add new script to {bank} - Bank is full.")
        data = bytearray.fromhex(data)
        targetIndex = _findNextIndex(0, 256, self.banks[bank])
        _tryToAdd(self.banks[bank], targetIndex)

    def insertIntoScript(self, bank:int, scriptId:int, position:int, data:str):
        self.banks[bank][scriptId][position:position] = bytearray.fromhex(data)

    def insertIntoScriptAtEnd(self, bank:int, scriptId:int, data:str):
        self.insertIntoScript(bank, scriptId, len(self.banks[bank][scriptId])-1, data)

    def replaceScript(self, bank:int, scriptId:int, data:str):
        self.banks[bank][scriptId] = bytearray.fromhex(data)

    def findScriptByBytes(self, data:str)->list:
        data = bytearray.fromhex(data)
        scriptList = []
        for bank in self.banks:
            for k,v in bank.items():
                for i in range (0, (len(v) - len(data) + 1)):
                    if v[i:len(data)+i] == data:
                        scriptList.append([self.banks.index(bank), k, i])
        return scriptList

    def removeFromScript(self, bank:int, scriptId:int, positionStart:int, positionEnd:int):
        del self.banks[bank][scriptId][positionStart:positionEnd]