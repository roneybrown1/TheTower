import Game
import random


class Armor:
    def __init__(self, aLvl, aClassType, aName, aType, aBaseDef, aBaseEvd, aDur):
        self.level = aLvl
        self.classtype = aClassType
        self.type = aType
        self.name = aName

        chance = random.randint(1, 100)

        if chance < 20:
            self.quality = 'Rusty'
        elif chance >= 21 or chance < 65:
            self.quality = 'Common'
        elif chance >= 66 or chance < 86:
            self.quality = 'Great'
        elif chance >= 85 or chance < 96:
            self.quality = 'Magical'
        elif chance >= 96 or chance < 100:
            self.quality = 'Legendary'

        self.basedefn = armorbasedef
        if self.quality == 'Rusty':
            self.basedefn = int(self.basedefn * 0.9)
        elif self.quality == 'Common':
            self.basedefn = int(self.basedefn * 1)
        elif self.quality == 'Great':
            self.basedefn = int(self.basedefn * 1.25)
        elif self.quality == 'Magical':
            self.basedefn = int(self.basedefn * 1.6)
        elif self.quality == 'Legendary':
            self.basedefn = int(self.basedefn * 2)

        self.defn = self.basedefn
        self.maxdur = armordur
        if self.quality == 'Rusty':
            self.maxdur = int(self.maxdur * 0.9)
        elif self.quality == 'Common':
            self.maxdur = int(self.maxdur * 1)
        elif self.quality == 'Great':
            self.maxdur = int(self.maxdur * 1.25)
        elif self.quality == 'Magical':
            self.maxdur = int(self.maxdur * 1.6)
        elif self.quality == 'Legendary':
            self.maxdur = int(self.maxdur * 2)
        self.dur = self.maxdur

    def damagedur(self, aug, curve):
        self.dur -= int(aug * curve * .1)
        self.isbroken()
        pass

    def restoredur(self, aug):
        self.dur += aug
        if self.dur > self.maxdur:
            self.dur = self.maxdur
        if not self.isbroken():
            self.defn = self.basedefn

    def repair(self):
        self.defn = self.basedefn
        self.dur = self.maxdur

    def isbroken(self):
        if self.dur <= 0:
            self.gearbreak()
            return True
        elif self.dur > 0:
            return False

    def gearbreak(self):
        self.atk = int(self.basedefn * .3)

    def printarmorinfo(self):
        print('ARMOR')
        print(('Level:', str(self.level), 60))
        print(('Name:', str(self.name), 60))
        print(('Type:', str(self.type), 60))
        print(('Defense:', str(self.defn) + '/' + str(self.basedefn), 60))
        print(('Dur:', str(self.dur) + '/' + str(self.maxdur), 60))
        print(('Broken?:', str(self.isbroken()), 60))
        print(('Quality:', str(self.quality()), 60))

    def datadict(self):
        return {'Level': str(self.level),
                'Name': str(self.name) + ' ' + str(self.type),
                'Def': str(self.defn),
                'Dur': str(self.dur) + '/' + str(self.maxdur),
                'Broken?': str(self.isbroken()),
                'Repair Cost': str(self.maxdur - self.dur) + ' Rupines',
                'Quality': str(self.quality)
                }