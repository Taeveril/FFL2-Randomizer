import mmap
from FFL2R_utils import Utility

class MonsterManager:
    def __init__ (self, rom:mmap):
        self.FAMILY = 0x33800
        self.AI = 0x33d50
        self.GFX = 0x36400
        self.NPC = 0x36b70
        self.STATS = 0x36f80
        self.NAME = 0x3eec0
        self.GOLD = 0x33c50
        self.monster = self._populateMonsters(rom)

    def _populateMonsters(self, rom:mmap)->dict:
        d = {}
        for m in range(0,256):
            stats = bytearray()
            for x in range(0,10):
                stats.append(rom[self.STATS+(m*10)+x])
            name = bytearray()
            for y in range(0,8):
                name.append(rom[self.NAME+((m*8)+y)])
            skills = bytearray()
            skillLoc = Utility.twoBytes(stats[8], stats[9]) + 0x30000
            skillLength = (stats[0] & 0x0f) + 1
            for l in range(0, skillLength):
                skills.append(rom[skillLoc + l])
            d[m] = self.Monster(rom[self.FAMILY+m], rom[self.AI+m], rom[self.GFX+m], rom[self.NPC+m], self.STATS + (m * 10), stats, 
                                self.NAME+(m*8), name, skillLoc, skillLength,skills, rom[self.GOLD+m])
        return d

    class Monster:
        def __init__(self, monsterFamily:int, monsterAI:int, monsterGFX:int, monsterNPC:int, statAddr:int, stats:list, nameAddr:int, name:list, 
                     skillLoc:int, skillLength:int, skills:list, goldIndex:int):
            self.family = monsterFamily
            self.ai = monsterAI
            self.gfx = monsterGFX
            self.npc = monsterNPC
            self.statAddr = statAddr
            self.stats = stats
            self.skillsLoc = skillLoc
            self.skillsLength = skillLength
            self.skills = skills
            self.nameAddr = nameAddr
            self.name = name
            self.dslevel = self.ai & 0x0f
            self.goldIndex = goldIndex #low nibble is the reference, plus first bit of high nibble (24 entries)
                                       #high nibble: 2nd bit = rare drop, 3rd bit = common drop, 4th bit = meat flag

        def info(self):
            print(f"""            
            Name:           {Utility.dteTranslate(self.name)}
            Name Addr:      {hex(self.nameAddr)}
            Monster Family: {self.family}
            AI:             {self.ai}
            GFX:            {self.gfx}
            NPC:            {self.npc}
            Stat Addr:      {hex(self.statAddr)}
            Stats:          {self.stats.hex(" ")}
            Skills Loc:     {hex(self.skillsLoc)}
            Skill Length:   {self.skillsLength}
            Skills:         {self.skills.hex(" ")}            
            DS Level:       {self.dslevel}
            Gold Index:     {self.goldIndex}
            """
            )