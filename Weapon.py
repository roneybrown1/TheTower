import random


class Weapon:
    # Setting up Level, Class, Name, Type, Base Attack, Durability, Special Attribute.
    def __init__(self, wLvl, wClass, wName, wType, wBaseAtk, wDur, wSpecial):
        # Weapon level
        self.lvl = wLvl

        # Weapon hero class type
        self.pClass = wClass

        # Weapon Type
        self.type = wType

        # Weapon Name
        self.name = wName

        # Weapon Quality (Weak, Old, Novice, Bronze, Iron, Steel, Reinforced, War, Ancient, Enchanted,
        # Glowing, Epic, Mythical)
        chance = random.randint(1, 265)

        if chance < 20:
            self.quality = 'Weak'
        elif chance >= 40 or chance < 45:
            self.quality = 'Old'
        elif chance >= 60 or chance < 65:
            self.quality = 'Novice'
        elif chance >= 80 or chance < 85:
            self.quality = 'Bronze'
        elif chance >= 100 or chance < 105:
            self.quality = 'Iron'
        elif chance >= 120 or chance < 125:
            self.quality = 'Steel'
        elif chance >= 140 or chance < 145:
            self.quality = 'Reinforced'
        elif chance >= 160 or chance < 165:
            self.quality = 'War'
        elif chance >= 180 or chance < 185:
            self.quality = 'Ancient'
        elif chance >= 200 or chance < 205:
            self.quality = 'Enchanted'
        elif chance >= 220 or chance < 225:
            self.quality = 'Glowing'
        elif chance >= 240 or chance < 245:
            self.quality = 'Epic'
        elif chance >= 260 or chance < 265:
            self.quality = 'Mythical'

        # Weapon atk
        self.baseAtk = wBaseAtk
        if self.quality == 'Weak':
            self.baseAtk = int(self.baseAtk * 0.2)
        elif self.quality == 'Old':
            self.baseAtk = int(self.baseAtk * 0.6)
        elif self.quality == 'Novice':
            self.baseAtk = int(self.baseAtk * 1)
        elif self.quality == 'Bronze':
            self.baseAtk = int(self.baseAtk * 1.4)
        elif self.quality == 'Iron':
            self.baseAtk = int(self.baseAtk * 1.8)
        elif self.quality == 'Steel':
            self.baseAtk = int(self.baseAtk * 2.2)
        elif self.quality == 'Reinforced':
            self.baseAtk = int(self.baseAtk * 2.6)
        elif self.quality == 'War':
            self.baseAtk = int(self.baseAtk * 3.0)
        elif self.quality == 'Ancient':
            self.baseAtk = int(self.baseAtk * 3.4)
        elif self.quality == 'Enchanted':
            self.baseAtk = int(self.baseAtk * 3.8)
        elif self.quality == 'Glowing':
            self.baseAtk = int(self.baseAtk * 4.2)
        elif self.quality == 'Epic':
            self.baseAtk = int(self.baseAtk * 4.6)
        elif self.quality == 'Mythical':
            self.baseAtk = int(self.baseAtk * 4.8)

        self.atk = self.baseAtk

        # Weapon durability
        self.maxDur = wDur
        self.dur = self.maxDur

        # Weapon Power (Not implemented yet)
        self.special = wSpecial

    # damage durability, and check to see if broken
    def damagedur(self, aug, curve):
        self.dur -= int(aug * curve * .1)
        self.isBroken()
        pass

    # restore dur by integer and check to see if fixed
    def restoredur(self, aug):
        self.dur += aug
        if not self.isBroken():
            self.dur = self.maxDur
            self.atk = self.baseAtk

    # restore dur entirely
    def repair(self):
        self.atk = self.baseAtk
        self.dur = self.maxDur

    # this breaks the gear
    def gearbreak(self):
        self.atk = int(self.baseAtk * .3)

    # 15% durability = stat reduction
    def isBroken(self):
        if self.dur <= 0:
            self.gearbreak()
            return True
        elif self.dur >= self.maxDur * .15:
            return False

    # prints all weapon stats
    def printweaponinfo(self):
        print('WEAPON')
        print(('Level:', str(self.lvl), 70))
        print(('Class:', str(self.pClass), 70))
        print(('Name:', str(self.name), 70))
        print(('Type:', str(self.type), 70))
        print(('Atk:', str(self.atk) + '/' + str(self.baseAtk), 70))
        print(('Dur:', str(self.dur) + '/' + str(self.maxDur), 70))
        print(('Status:', str(self.isBroken()), 70))
        print(('Special:', str(self.special), 70))
        print(('Quality:', str(self.quality), 70))

    # ['Level', 'Name', 'Type', 'Atk', 'Dur', 'Broken?', 'Power']
    def datadict(self):
        return {'Level': str(self.lvl),
                'Name': (str(self.name) + ' ' + str(self.type)),
                'Atk': str(self.atk),
                'Dur': (str(self.dur) + '/' + str(self.maxDur)),
                'Status': str(self.isBroken()),
                'Repair Cost': str(self.maxDur - self.dur) + ' gold',
                'Special': str(self.special),
                'Quality': str(self.quality)
                }
