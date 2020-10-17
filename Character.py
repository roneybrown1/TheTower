import Game
import Commands
import Armor
import Weapon
import Item
from art import *


class Character:
    def __init__(self, pClass, pLvl, pHP, pMP, pAtk, pDef, pEvd, pNxtLvl):
        # Character Stats.
        self.name = ''
        self.pClass = pClass
        self.level = pLvl
        self.nxtLvl = pNxtLvl
        self.HP = pHP
        self.maxHP = self.HP
        self.MP = pMP
        self.maxMP = self.MP
        self.atk = self.baseAtk
        self.baseAtk = pAtk
        self.defe = self.baseDefe
        self.baseDefe = pDef
        self.evd = self.baseEvd
        self.baseEvd = pEvd
        self.luck = self.baseLuck
        self.baseLuck = 0
        self.crit = self.baseCrit
        self.baseCrit = 0
        self.gold = 0
        self.exp = 0
        self.hpAug = 0
        self.mpAug = 0
        self.atkAug = 0
        self.defeAug = 0
        self.evdAug = 0
        self.lvlUpAug = 0
        self.critAug = 0

        # Character item setup.
        self.items = []
        self.activeItem = 0
        self.gear = []

        # Character class attack and defense curve.
        self.atkCurve = 0
        self.defeCurve = 0

        # Weapon, Armor, Items, and Character state setup.
        self.pWeapon = Weapon.Weapon(0, 'Beginner', 'Stick', 'Wooden', 2, 8, 'None')
        self.pArmor = Armor.Armor(0, 'Beginner', 'Peasant Clothes', 'Cloth', 5, 3, 8)
        self.pItem = Item.Item(0, 0, 0, 0, 0)
        self.isFighting = False

    def heal(self, hpUp):
        print(str(self.name) + ' heal for ' + str(int(hpUp)) + ' HP!')
        print('')
        self.HP += hpUp
        if self.HP > self.maxHP:
            self.HP = self.maxHP

    def food(self):
        hpBack = int(self.maxHP * .2)
        print(str(self.name) + ' found a piece of bread and healed ' + str(hpBack) + ' HP!')
        self.heal(hpBack)

    def mana(self, mpUp):
        print(str(self.name) + ' regenerated ' + str(int(mpUp)) + ' MP!')
        print('')
        self.MP += mpUp
        if self.MP > self.maxMP:
            self.MP = self.maxMP

    def manaherb(self):
        mpBack = int(self.maxMP * .2)
        print(str(self.name) + ' found a weak mana herb and regenerated ' + str(mpBack) + ' MP!')
        self.mana(mpBack)

    def damage(self, hpDown):
        effatk = hpDown + (hpDown * self.defeCurve)
        self.HP -= int(effatk)
        print(str(self.name) + 'takes ' + str(int(effatk)) + ' damage!')
        if self.HP < 0:
            self.HP = 0

    def death(self):
        self.isFighting = False
        self.HP = 0
        tprint("You Died....")
        print(str(self.name) + ' tried their hardest but was overcome by the power of the beastlie...\n' +
              str(self.name) + '%s has been slain and their soul sent to rest in the gates of Norgalhelm\n.' +
              'Poor' + str(self.name) + ', their mother had high hopes that they would become a great and\n' +
              'strong adventurer but the beastlies had other plans for them. Rest well ' + str(self.name) +
              ' maybe you will be reincarnated as a capable adventure.')
        tprint("Game Over.")

    def addexp(self, gainedexp):
        gainedexp = gainedexp + (gainedexp * self.defeCurve)
        print(str(self.name) + ' gained' + str(int(gainedexp)) + ' Exp.')
        self.exp += int(gainedexp)
        if self.exp >= self.nxtLvl:
            self.levelup()

    def addgold(self, gainedgold):
        gainedgold = gainedgold + (gainedgold * self.defeCurve)
        print(str(self.name) + ' gained' + str(int(gainedgold + (gainedgold * self.defeCurve))) + ' Rupines!')
        self.gold += int(gainedgold + (gainedgold * self.defeCurve))

    def classAttributes(self):
        # Base game classes and subclasses.
        if self.pClass == 'Fighter':
            self.hpAug = 15
            self.mpAug = 3
            self.evdAug = 2
            self.defeAug = 12
            self.atkAug = 2
            self.lvlUpAug = 1
            self.critAug = 2
        elif self.pClass == 'Apprentice':
            self.hpAug = 5
            self.mpAug = 12
            self.evdAug = 5
            self.defeAug = 6
            self.atkAug = 12
            self.lvlUpAug = .6
            self.critAug = 2
        elif self.pClass == 'Scout':
            self.hpAug = 10
            self.mpAug = 5
            self.evdAug = 8
            self.defeAug = 8
            self.atkAug = 12
            self.lvlUpAug = .8
            self.critAug = 6
        elif self.pClass == 'Warrior':
            self.hpAug = 25
            self.mpAug = 9
            self.evdAug = 12
            self.defeAug = 22
            self.atkAug = 12
            self.lvlUpAug = 3
            self.critAug = 5
        elif self.pClass == 'Journeyman':
            self.hpAug = 15
            self.mpAug = 22
            self.evdAug = 15
            self.defeAug = 16
            self.atkAug = 22
            self.lvlUpAug = 2.6
            self.critAug = 5
        elif self.pClass == 'Hunter':
            self.hpAug = 20
            self.mpAug = 12
            self.evdAug = 18
            self.defeAug = 18
            self.atkAug = 22
            self.lvlUpAug = 2.8
            self.critAug = 9
        elif self.pClass == 'Knight':
            self.hpAug = 35
            self.mpAug = 14
            self.evdAug = 22
            self.defeAug = 32
            self.atkAug = 22
            self.lvlUpAug = 5
            self.critAug = 8
        elif self.pClass == 'Mage':
            self.hpAug = 25
            self.mpAug = 32
            self.evdAug = 35
            self.defeAug = 26
            self.atkAug = 32
            self.lvlUpAug = 4.6
            self.critAug = 8
        elif self.pClass == 'Strider':
            self.hpAug = 30
            self.mpAug = 20
            self.evdAug = 28
            self.defeAug = 28
            self.atkAug = 32
            self.lvlUpAug = 4.8
            self.critAug = 12
        elif self.pClass == 'Grand Master':
            self.hpAug = 45
            self.mpAug = 25
            self.evdAug = 32
            self.defeAug = 42
            self.atkAug = 32
            self.lvlUpAug = 7
            self.critAug = 11
        elif self.pClass == 'Arch Magus':
            self.hpAug = 35
            self.mpAug = 42
            self.evdAug = 45
            self.defeAug = 36
            self.atkAug = 42
            self.lvlUpAug = 6.6
            self.critAug = 11
        elif self.pClass == 'Ranger':
            self.hpAug = 40
            self.mpAug = 35
            self.evdAug = 38
            self.defeAug = 38
            self.atkAug = 42
            self.lvlUpAug = 6.8
            self.critAug = 15
        # Epic Classes. 2 Fighter, 2, Apprentice, 2 Scout.
        elif self.pClass == 'Paladin':
            self.hpAug = 65
            self.mpAug = 45
            self.evdAug = 62
            self.defeAug = 52
            self.atkAug = 62
            self.lvlUpAug = 9
            self.critAug = 14
        elif self.pClass == 'Echo Knight':
            self.hpAug = 65
            self.mpAug = 50
            self.evdAug = 52
            self.defeAug = 62
            self.atkAug = 52
            self.lvlUpAug = 9
            self.critAug = 18
        elif self.pClass == 'Necromancer':
            self.hpAug = 55
            self.mpAug = 60
            self.evdAug = 55
            self.defeAug = 46
            self.atkAug = 56
            self.lvlUpAug = 8.6
            self.critAug = 14
        elif self.pClass == 'Shadowknight':
            self.hpAug = 55
            self.mpAug = 55
            self.evdAug = 46
            self.defeAug = 56
            self.atkAug = 62
            self.lvlUpAug = 8.6
            self.critAug = 14
        elif self.pClass == 'Stalker':
            self.hpAug = 50
            self.mpAug = 50
            self.evdAug = 68
            self.defeAug = 58
            self.atkAug = 52
            self.lvlUpAug = 8.8
            self.critAug = 18
        elif self.pClass == 'Bounty Hunter':
            self.hpAug = 50
            self.mpAug = 55
            self.evdAug = 68
            self.defeAug = 48
            self.atkAug = 52
            self.lvlUpAug = 8.8
            self.critAug = 18
        self.HP += self.hpAug
        self.maxHP += self.hpAug
        self.MP += self.mpAug
        self.maxMP += self.mpAug
        self.evd += self.evdAug
        self.defe += self.defeAug
        self.baseDefe += self.defeAug
        self.nxtLvl = int(self.nxtLvl * self.lvlUpAug)
        self.atk += self.atkAug
        self.baseAtk += self.atkAug

    def printchardetails(self):
        print('Character Data')
        print('Name:', str(self.name))
        print('Class:', str(self.pClass))
        print('Level:', str(self.level))
        print('HP:', str(self.HP) + '/' + str(self.maxHP))
        print('MP:', str(self.MP) + '/' + str(self.maxMP))
        print('Attack:', str(self.atk))
        print('Defense:', str(self.defe))
        print('Evade:', str(self.evd))
        print('Exp:', str(self.exp) + '/' + str(self.nxtLvl))
        print('Rupines:', str(self.gold))

    def datadict(self):
        return {
            'Name': str(self.name),
            'Class': str(self.pClass),
            'Level': str(self.level),
            'HP': str(str(self.HP) + '/' + str(self.maxHP)),
            'MP:': str(str(self.MP) + '/' + str(self.maxMP)),
            'Attack': str(str(self.atk)),
            'Defense': str(str(self.defe)),
            'Evade': str(str(self.evd)),
            'Exp': str(str(self.exp) + '/' + str(self.nxtLvl)),
            'Rupines': str(str(self.gold))
        }

    def levelup(self):
        print(str(self.name) + 'Leveled Up!')
        self.exp -= self.nxtLvl
        self.level += 1
