import mmap
from FFL2R_data import GameData
from FFL2R_utils import Utility

class ShopManager:
        def __init__(self, rom:mmap):
            self._SHOP_STARTADDR = 0x3f9e0
            self._SHOP_ENDADDR = 0x3fa9f
            self.shop = self._populateShops(rom)

        def _populateShops(self, rom:mmap)->dict:
            d = {}
            indexer = 0
            name = ""
            i = self._SHOP_STARTADDR
            for x in range (self._SHOP_STARTADDR, self._SHOP_ENDADDR, 8):
                shopArray = bytearray()
                for i in range (0,8):
                    shopArray.append(rom[x+i])
                match x:
                    case 0x3f9e0:
                        tier = 1
                        name = "First Town, Weapon Shop"
                    case 0x3f9e8:
                        tier = 2
                        name = "Desert Town, Weapon Shop"
                    case 0x3f9f0:
                        tier = 2
                        name = "Ashura Town, Weapon Shop"
                    case 0x3f9f8:
                        tier = 3
                        name = "Giant Town, Weapon Shop"
                    case 0x3fa00:
                        tier = 1
                        name = "Second Town, Weapon Shop"
                    case 0x3fa08:
                        tier = 3
                        name = "Apollo Town, Weapon Shop"
                    case 0x3fa10:
                        tier = 4
                        name = "Lynn Town, Weapon Shop"
                    case 0x3fa18:
                        tier = 4
                        name = "Guardian Town, Weapon Shop"
                    case 0x3fa20:
                        tier = 5
                        name = "Venus Town, Weapon Shop"
                    case 0x3fa28:
                        tier = 5 
                        name = "Race Town, Weapon Shop"
                    case 0x3fa30:
                        tier = 6
                        name = "Edo Town, Weapon Shop"
                    case 0x3fa38:
                        tier = 6
                        name = "Final Town, Weapon Shop"
                    case 0x3fa40:
                        tier = 1
                        name = "First Town, Item Shop"
                    case 0x3fa48:
                        tier = 2
                        name = "Desert Town, Item Shop"
                    case 0x3fa50:
                        tier = 3
                        name = "Giant Town, Item Shop"
                    case 0x3fa58:
                        tier = 4
                        name = "Apollo Town, Item Shop"
                    case 0x3fa60:
                        tier = 4
                        name = "Guardian Town, Item Shop"
                    case 0x3fa68:
                        tier = 5
                        name = "Venus Town, Item Shop"
                    case 0x3fa70:
                        tier = 6
                        name = "Race Town, Item Shop"
                    case 0x3fa78:
                        tier = 6
                        name = "Edo Town, Item Shop"
                    case 0x3fa80:
                        tier = 7
                        name = "Post-Theft Shop, Item Shop"
                    case 0x3fa88:
                        tier = 0
                        name = "Recurring Item Shop"
                    case 0x3fa90:
                        tier = 8
                        name = "Echigoya"
                    case 0x3fa98:
                        tier = 9
                        name = "Giant Town Giant Gear Seller"
                    case _:
                        print("shop err.")
                d[indexer] = self.Shop(x, name, tier, shopArray)
                indexer+=1
            return d
        
        class Shop:
            def __init__(self, addr:int, name:str, tier:int, wares:list):
                self.addr = addr
                self.name = name
                self.tier = tier
                self.wares = wares

            def info(self):
                print(f"""
                Addr: {hex(self.addr)}
                Name:  {self.name}
                Tier:  {self.tier}
                Wares: {[GameData.items[item] for item in self.wares if item != 0xff] }
                """
                )

class GoldManager:
    def __init__ (self, rom:mmap):
        self._GT_STARTADDR = 0x33e50
        self._GT_ENDADDR = 0x33e7f
        self.dropValue = self._populateGold(rom)

    def _populateGold(self, rom:mmap)->dict:
        indexer = 0
        gt = {}
        for x in range(self._GT_STARTADDR, self._GT_ENDADDR, 2):
            gt[indexer] = self.GoldEntry(x, rom[x], rom[x+1])
            indexer+=1
        return gt

    class GoldEntry:
        def __init__(self, addr:int, firstByte:int, secondByte:int):
            self.addr = addr
            self.firstByte = firstByte
            self.secondByte = secondByte
            self.actualValue = Utility.twoBytes(self.firstByte, self.secondByte)

        def updateGold(self, newValue:int):
            self.firstByte, self.secondByte = Utility.byteizeTwo(newValue)

        def info(self):
                print(f"""                
                Addr: {hex(self.addr)}
                Amount: {self.actualValue}
                """
                )

class ItemManager:
    def __init__(self, rom:mmap):
        self.FLAGS = 0x32f80
        self.NAME = 0x3e640
        self.PRICE = 0x3f860
        self.USES = 0x33e80
        self.AFFINITIES = 0x33b40
        self.item = self._populateItems(rom)

    def _populateItems(self, rom:mmap)->dict:
        d = {}
        for x in range(0, 272):
            itemFlags = bytearray()
            for y in range (0,8):
                itemFlags.append(rom[self.FLAGS+(x*8)+y])
            itemName = bytearray()
            for y in range(0,8):
                itemName.append(rom[self.NAME+(x*8)+y])
            itemPrice = bytearray()
            if x < 128:
                for y in range(0,3):
                    itemPrice.append(rom[self.PRICE+(x*3)+y])
            else:
                itemPrice = None
            d[x] = self.Item(itemFlags, itemName, itemPrice, rom[self.USES+x], rom[self.AFFINITIES+x])
        return d

    class Item:
        def __init__(self, flags, name, price, use, affinities):
            self.flags = flags
            self.name = name
            self.price = price
            self.use = use
            self.affinities = affinities

        def setPrice(self, amount:int):
            p = Utility.byteizeThree(amount)
            self.price = bytearray.fromhex(f"{p[0]:02x}{p[1]:02x}{p[2]:02x}")

        def info(self):
            print(f"""
            Name:           {Utility.dteTranslate(self.name)}
            Uses:           {self.use}
            Price:          {Utility.threeBytes(self.price[0], self.price[1], self.price[2])}
            Script:         {self.flags[3]}
            Robot Power:    {Utility.lowNibble(self.affinities)}
            Anim:           {self.flags[6]}
            Sound:          {self.flags[7]}
            Param1:         {self.flags[4]}
            Param2:         {self.flags[5]}
                Target All:         {Utility.isbitset(Utility.highNibble(self.flags[0]), 0)}
                Target Enemy:       {Utility.isbitset(Utility.highNibble(self.flags[0]), 1)}
                Flag7:              {Utility.isbitset(Utility.highNibble(self.flags[0]), 2)}
                Melee:              {Utility.isbitset(Utility.highNibble(self.flags[0]), 3)}
                In Battle:          {Utility.isbitset(Utility.lowNibble(self.flags[0]), 0)}
                In Menu:            {Utility.isbitset(Utility.lowNibble(self.flags[0]), 1)}
                Can't Unequip:      {Utility.isbitset(Utility.lowNibble(self.flags[0]), 2)}
                Flag4:              {Utility.isbitset(Utility.lowNibble(self.flags[0]), 3)}
                Reflect:            {Utility.isbitset(Utility.highNibble(self.flags[1]), 0)}
                Element Magi:       {Utility.isbitset(Utility.highNibble(self.flags[1]), 1)}
                Warning:            {Utility.isbitset(Utility.highNibble(self.flags[1]), 2)}
                Surprise:           {Utility.isbitset(Utility.highNibble(self.flags[1]), 3)}
                Counter:            {Utility.isbitset(Utility.lowNibble(self.flags[1]), 0)}
                Skin:               {Utility.isbitset(Utility.lowNibble(self.flags[1]), 1)}
                Burning:            {Utility.isbitset(Utility.lowNibble(self.flags[1]), 2)}
                Shield:             {Utility.isbitset(Utility.lowNibble(self.flags[1]), 3)}
                Resist:             {Utility.isbitset(Utility.highNibble(self.flags[2]), 0)}
                Weakness:           {Utility.isbitset(Utility.highNibble(self.flags[2]), 1)}
                Stat Bonus:         {Utility.isbitset(Utility.highNibble(self.flags[2]), 2)}
                Infinite:           {Utility.isbitset(Utility.highNibble(self.flags[2]), 3)}
                Helmet:             {Utility.isbitset(Utility.lowNibble(self.flags[2]), 0)}
                Body:               {Utility.isbitset(Utility.lowNibble(self.flags[2]), 1)}
                Gauntlet:           {Utility.isbitset(Utility.lowNibble(self.flags[2]), 2)}
                Shoes:              {Utility.isbitset(Utility.lowNibble(self.flags[2]), 3)}
                Poison/Def Bonus:   {Utility.isbitset(Utility.lowNibble(self.flags[5]), 0)}
                Thunder/Mana Bonus: {Utility.isbitset(Utility.lowNibble(self.flags[5]), 1)}
                Ice/Agi Bonus:      {Utility.isbitset(Utility.lowNibble(self.flags[5]), 2)}
                Fire/Str Bonus:     {Utility.isbitset(Utility.lowNibble(self.flags[5]), 3)}
                Quake:              {Utility.isbitset(Utility.highNibble(self.flags[5]), 0)}
                Weapon:             {Utility.isbitset(Utility.highNibble(self.flags[5]), 1)}
                Stone:              {Utility.isbitset(Utility.highNibble(self.flags[5]), 2)}
                Paralysis:          {Utility.isbitset(Utility.highNibble(self.flags[5]), 3)}
                Def Affinity:       {Utility.isbitset(Utility.highNibble(self.affinities), 0)}
                Mana Affinity:      {Utility.isbitset(Utility.highNibble(self.affinities), 1)}
                Agi Affinity:       {Utility.isbitset(Utility.highNibble(self.affinities), 2)}
                Str Affinity:       {Utility.isbitset(Utility.highNibble(self.affinities), 3)}
            """
            )
