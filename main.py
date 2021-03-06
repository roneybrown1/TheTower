from art import *
import sys
import os
import csv
import json
import random
from random import randint


# Variables
save_state = True
weapons = {"Rapier": 40, "Sabre": 50, "Cutlass": 60, "Scimitar": 70, "Long Sword": 90, "Bastard Sword": 120,
           "Great Sword": 150}


class Item(object):
    def __init__(self, name, strvalue, evdvalue):
        self.name = name
        self.strvalue = strvalue
        self.evdvalue = evdvalue


class Character:
    def __init__(self):
        self.name = ""
        self.state = 'normal'
        self.hp = 50
        self.hp_max = 50
        self.lvl = 1
        self.base_attack = 10
        self.base_def = 15
        self.base_def_max = 15
        self.base_evade = 10
        self.base_evade_max = 10
        self.gold = 0
        self.gold_max = 1000
        self.pots = 0
        self.weap = ["Rusty Sword", "Rusty Dagger", " Wooden Bow", "Fist"]
        self.weapons = ['Rapier', 'Sabre', 'Cutlass', 'Scimitar', 'Long Sword', 'Bastard Sword', 'Great Sword']
        self.curweap = 'none'
        self.inventory = []

    def do_damage(self, enemy):
        damage = min(max(randint(0, self.base_attack) - randint(0, enemy.hp), 0),
                     enemy.hp, self.base_def, self.base_evade) * 2
        enemy.hp = enemy.hp - damage
        if damage == 0:
            print("%s was able to evade %s's \033[1;31;1mattack\033[1;37;1m." % (enemy.name, self.name))
            print("\033[1;31;1m""0 damage""\033[1;37;1m taken.")
        else:
            print("%s landed a \033[1;31;1mdamaging\033[1;37;1m blow on %s."
                  % (self.name, enemy.name))
            print("\033[1;31;1m" + str(damage) + "\033[1;31;1m", "\033[1;37;1mdamage was dealt!")
            return enemy.hp <= 0


class Enemy(Character):
    def __init__(self, player):
        Character.__init__(self)
        first = ("Giant", "Fire-Eyed", "Half-Dead", "Rotting", "Bloated", "Hulking", "Grizzly", "Angered", "Injured",
                 "Erratic", "Frenzied", "Yellow", "Red", "Black", "Wasting", "Gross", "Ghastly", "Demonic", "Doomed",
                 "Savage", "Stone", "Elemental", "Abyssal", "Plague", "Behemoth", "Gelatinous", "Zombie", "Oozing",
                 "Lesser", "Fabled", "Fiendish", "Possessed", "Enraged", "Corrupted", "Forsaken", "Putrid", "Rabid",
                 "Vile")
        second = ("Goblin", "Warlock", "Witch", "Minotaur", "Kobald", "Skeleton", "Ogre", "Rat", "Spirit", "Troll",
                  "Vampire", "Banshee", "Warrior", "Dog", "Spider", "Snake", "Harpy", "Specter", "Dwarf", "Hobgoblin",
                  "Bat", "Familiar", "Golem", "Thief", "Orc", "Halfling", "Drow", "pixie", "Satyr", "Imp", "Hag",
                  "Lich", "Crawler", "Wasp", "Mage", "Slime")
        titleOne = random.choice(first)
        titleTwo = random.choice(second)
        self.name = (titleOne + " " + titleTwo)
        self.hp = random.randint(1, player.hp) * 2
        self.base_attack = 15
        self.base_def = 10
        self.base_evade = 10


class Boss(Character):
    def __init__(self, player):
        Character.__init__(self)
        name = ("Ur", "Grog", "Shagu", "Orior", "Tork", "Isha", "Ulma", "Rago", "Hork", "Palu", "Dar", "Kilu", "Fuz",
                "Quer", "Masq", "P'Luah", "Y'Esha", "O'tru", "Fert", "Unah", "Zuul", "Jatur", "Yent", "Oki", "Nort",
                )
        first = ("Giant", "Fire-Eyed", "Half-Dead", "Rotting", "Bloated", "Hulking", "Grizzly", "Angered", "Injured",
                 "Erratic", "Frenzied", "Yellow", "Red", "Black", "Wasting", "Gross", "Ghastly", "Demonic", "Doomed",
                 "Savage", "Stone", "Elemental", "Abyssal", "Plague", "Behemoth", "Gelatinous", "Zombie", "Oozing",
                 "Lesser", "Fabled", "Fiendish", "Possessed", "Enraged", "Corrupted", "Forsaken", "Putrid", "Rabid",
                 "Vile")
        second = ("Goblin", "Warlock", "Witch", "Minotaur", "Kobald", "Skeleton", "Ogre", "Rat", "Spirit", "Troll",
                  "Vampire", "Banshee", "Warrior", "Dog", "Spider", "Snake", "Harpy", "Specter", "Dwarf", "Hobgoblin",
                  "Bat", "Familiar", "Golem", "Thief", "Orc", "Halfling", "Drow", "pixie", "Satyr", "Imp", "Hag",
                  "Lich", "Crawler", "Wasp", "Mage", "Slime")
        name = random.choice(name)
        titleOne = random.choice(first)
        titleTwo = random.choice(second)
        self.name = (name + " " + titleOne + " " + titleTwo)
        self.hp = random.randint(1, 300) * 2
        self.base_attack = 60
        self.base_def = 70
        self.base_evade = 40


class Player(Character):
    def __init__(self):
        Character.__init__(self)
        self.state = 'normal'
        self.hp = 50
        self.hp_max = 50
        self.lvl = 1
        self.exp = 0
        self.nextLvl = self.nextLvl
        self.base_attack = 10
        self.base_def = 15
        self.base_def_max = 15
        self.base_evade = 10
        self.base_evade_max = 10
        self.gold = 0
        self.gold_max = 1500
        self.pots = 0
        self.weap = {}
        self.curweap = "none"
        self.inventory = []
        self.treasure_found = False

    def save(self):
        if self.state != 'normal':
            print("You cannot save at this time!")
            self.enemy_attacks()
        else:
            answer = input("Do you want to save the game? y/n ")
            save_state = True
            if answer == 'y' or answer == 'yes' or answer == 'Y' or answer == 'Yes':
                print("Preparing to save game")
                save_name = input("savename: ")
                path = ('saves/' + save_name + '.json')

                data = {
                    'savename': save_name, 'name': self.name, 'lvl': self.lvl, 'hp': self.hp, 'hp_max': self.hp_max,
                    'base_atk': self.base_attack, 'base_def': self.base_def, 'base_def_max': self.base_def_max,
                    'base_evade': self.base_evade, 'base_evade_max': self.base_evade_max, 'curweap': self.curweap,
                    'gold': self.gold, 'gold_max': self.gold_max, 'pots': self.pots, 'exp': self.exp
                }
                with open(path, 'w+') as f:
                    json.dump(data, f)
                print ('System: Saved ' + save_name + ' in ' + path)
                print ('The game has been saved, please type your next command to continue!')
            elif answer == 'n' or answer == 'no' or answer == 'N' or answer == 'No':
                return ()

    def quit(self):
        print("%s could not handle the stress of being alone, they sat behind\n"
              "a rock pulling their knees to their chest, closed their eyes\n"
              "and faded away into nothingness... Sleep well sweet %s, you\n"
              "tried your hardest..." % (self.name, self.name))
        exit()

    def help(self):
        print(Commands.keys())

    def status(self):
        print("%s's current stats are...\n Level: %s\n Health: %d/%d\n Exp: %s\n Attack: %s\n "
              "Def: %d/%d\n Evade: %d/%d\n Weapon: %s\n Gold: %d/%d\n Potions: %s"
              % (self.name, self.lvl, self.hp, self.hp_max, self.exp, self.base_attack,
                 self.base_def, self.base_def_max, self.base_evade, self.base_evade_max,
                 self.curweap, self.gold, self.gold_max, self.pots))

    def tired(self):
        print("%s can feel themselves getting weaker, one hp and evade point lost.\n"
              "You are tired and needs to rest." % self.name)
        self.hp = max(1, self.hp - 1)
        self.base_evade = max(1, self.base_evade - 1)

    def rest(self):
        if self.state != 'normal':
            print("%s cannot rest at this time!" % self.name)
            self.enemy_attacks()
        else:
            print("%s finds a place to settle, they brush any dirt and debris away.\n"
                  "Taking their satchel using it as a pillow, %s drift off to sleep.\n"
                  "%s is refreshed, gained one hp and evade point." % (self.name, self.name, self.name))
        if random.randint(0, 1):
            self.enemy = Enemy(self)
            print("A quick scuttle of feet/legs awakens %s from their sleep, before\n"
                  "they can react they are \033[1;31;1mattacked\033[0;37;1m" " by a(n) %s."
                  % (self.name, self.enemy.name))
            self.state = 'fight'
            self.enemy_attacks()
        else:
            if self.hp < self.hp_max:
                self.hp = self.hp + 1
            if self.base_evade < self.base_evade_max:
                self.base_evade = self.base_evade + 1

            else:
                print("%s has overslept causing them to feel drowsy, one hp and evade\n"
                      "points lost." % self.name)
                self.hp = self.hp - 1
                self.base_evade = self.base_evade - 1

    def explore(self):
        if self.state != 'normal':
            print("Are you insane?! %s is being attack by a %s and cannot continue exploring...\n"
                  "FOCUS! If you are not ready to take on this beastlie, you can \033[1;34;1m'flee'\033[1;37;1m."
                  % (self.name, self.enemy.name))
            self.enemy_attacks()
        else:
            print("%s moves cautiously through the twisting and turning tunnels of the cave,\n"
                  "with each step the cave seems to be alive and changing. %s continues forward."
                  % (self.name, self.name))
            if random.randint(0, 5) > 1:
                print("%s sees an opening in the cave wall, there is a faint glimmer in the distance.\n"
                      % self.name)
                answer = input("Explore the opening? y/n: ")
                if answer == 'y' or answer == 'yes' or answer == 'Y' or answer == 'Yes':
                    if random.randint(0, 5) > 1:
                        self.treasure_found = True
                        print("%s moves through the opening and towards the glimmer, moving closer %s and see\n"
                              "a treasure chest covered in strange symbols." % (self.name, self.name))
                        answer = input("Do you want to open the chest? y/n: ")
                        if answer == 'y' or answer == 'yes' or answer == 'Y' or answer == 'Yes':
                            print("%s slowly opens the chest, as they do they reveal...." % self.name)
                            if random.randint(0, 5) > 1:
                                if random.randint(0, 5) > 1:
                                    foundweapon = random.choice(self.weapons)
                                    print("A shimmering %s!" % foundweapon)
                                    random.choice(self.weapons)
                                    if foundweapon == self.curweap:
                                        print("%s already has this weapon equipped, %s has been added to your\n"
                                              "inventory." % (self.name, foundweapon))
                                        self.inventory.append(foundweapon)
                                    elif foundweapon != self.curweap:
                                        answer = input("Do you want to equip the item? y/n: ")
                                        if answer == 'y' or answer == 'yes' or answer == 'Y' or answer == 'Yes':
                                            print("%s has unequipped the %s and equipped the %s"
                                                  % (self.name, self.curweap, foundweapon))
                                            print("% has been placed in your inventory." % self.curweap)
                                            self.inventory.append(self.curweap)
                                            self.curweap = foundweapon
                                        elif answer == 'n' or answer == 'no' or answer == 'N' or answer == 'No':
                                            print("The item has been added to your inventory.")
                                            self.inventory.append(foundweapon)
                            elif random.randint(0, 20) < 10:
                                print("25 gold pieces!")
                                self.gold = self.gold + 25
                            else:
                                print("The chest was empty, someone or something must have gotten here first.\n"
                                      "%s continues exploring the cave." % self.name)
                        elif answer == 'n' or answer == 'no' or answer == 'N' or answer == 'No':
                            print("%s decides to not open the chest and continue exploring." % self.name)
                else:
                    print("The opening led %s into more caves, %s continues forward." % (self.name, self.name))
                    self.treasure_found = False
                if random.randint(0, 250) > 200:
                    print("As %s moved through the save they notice a skeleton tucked away in a dark crevice."
                          % self.name)
                    self.treasure_found = True
                    answer = input("Do you want to check the skeleton? y/n")
                    if answer == 'y' or answer == 'yes' or answer == 'Y' or answer == 'Yes':
                        print("%s moves closer to the skeleton, as they step closer to the decrepit remains they\n"
                              "notice a satchel." % self.name)
                        if random.randint(0, 50) > 25:
                            self.treasure_found = True
                            print("Reaching down into the satchel %s finds....\n" % self.name)
                            if randint(0, 3) == 1:
                                print("\033[1;32;1m100 gold pieces\033[1;37;1m! %s quickly takes the gold and\n"
                                      "places it in their gold bag. %s continues their adventure."
                                      % (self.name, self.name))
                                if self.gold != self.gold_max:
                                    self.gold = self.gold = 100
                                else:
                                    print("Unfortunately %s gold bag is full and cannot hold anymore.\n"
                                          "%s leaves the gold for another adventurer." % (self.name, self.name))
                            if randint(0, 3) == 2:
                                print("nothing, it seems that someone or something has already cleared the\n"
                                      "satchel of it's belonging. %s continues on their adventure." % self.name)
                            if randint(0, 3) == 3:
                                print("\033[1;32;1m3 health potions\033[1;37;1m! %s quickly takes the gold\n"
                                      "and places it in their gold bag. %s continues their adventure."
                                      % (self.name, self.name))
                                self.pots = self.pots + 3
                        else:
                            self.treasure_found = False
                            self.enemy = Enemy(self)
                            print("As %s reaches down to explore the contents of the satchel they\n"
                                  "are \033[1;31;1mattacked\033[0;37;1m from behind by a(n) %s!"
                                  % (self.name, self.enemy.name))
                            self.state = 'fight'
                            self.enemy_attacks()
                    if answer == 'n' or answer == 'no' or answer == 'N' or answer == 'No':
                        print("%s decides to let the poor soul rest in peace and continued their adventure."
                              % self.name)

        if random.randint(0, 25):
            self.treasure_found = False
            self.enemy = Enemy(self)
            print("As %s moves through the cave they notice a scuttling sound coming from behind them.\n"
                  "Oh no! %s has been \033[1;31;1mattacked\033[0;37;1m by a(n) %s!"
                  % (self.name, self.name, self.enemy.name))
            self.state = 'fight'
        else:
            if self.state != 'fight':
                if random.randint(0, 1):
                    self.tired()

    def flee(self):
        if self.state != 'fight':
            print("Oh....Okay...There is nothing to flee from, but I won't stop you %s..." % self.name)
            self.tired()
        else:
            if randint(1, self.hp + 5) > randint(1, self.enemy.hp):
                print("Unsure if they wanted to take on the challenger %s searches around for\n"
                      "an escape route seeing an opening %s dashes towards the enemy's blindside\n"
                      "and escaped into the darkness from the %s.\n"
                      "(Careful, this action reduces defense.)"
                      % (self.name, self.name, self.enemy.name))
                self.base_def = self.base_def - 1
                self.enemy = None
                self.state = 'normal'
            else:
                print("%s couldn't escape from the %s and is forced to continue the battle.\n"
                      "You can try to \033[1;34;1m'flee'\033[1;37;1m again or \033[1;31;1m'attack'\033[1;37;1m\n"
                      "the beastlie with your %s."
                      % (self.name, self.enemy.name, self.curweap))
                self.enemy_attacks()

    def attack(self):
        if self.state != 'fight':
            print("%s twirls about swinging their %s at absolutely nothing... Some would\n"
                  "say this is insane but %s is free to do as they will even if it is fruitless\n"
                  "and tiring." % (self.name, self.curweap, self.name))
            self.tired()
        else:
            if self.do_damage(self.enemy):
                print("%s readies themselves and with the right timing %s lands a \033[1;31;1mkilling\033[1;37;1m\n"
                      "blow on the %s!"
                      % (self.name, self.name, self.enemy.name))
                self.enemy = None
                self.state = 'normal'
                self.addexp()
                self.nextLvl()
                if random.randint(0, self.gold) < 10:
                    self.gold = self.gold + 5
                    print("%s found five gold pieces! Cha-ching!" % self.name)
                    if random.randint(0, self.pots) < 5:
                        self.pots = self.pots + 1
                        print("%s found one health potion!" % self.name)
                        if random.randint(0, 40) > 40:
                            print("%s found a %s!" % (self.name, random.choice(self.weapons)))
                            self.weap = random.choice(self.weapons)
                print(self.status())

            else:
                self.enemy_attacks()

    def enemy_attacks(self):
        if self.enemy.do_damage(self):
            print("%s tried their hardest but was overcome by the power of the %s... %s has been slain\n"
                  "and their soul sent to rest. Poor %s, their mother had high hopes that they would\n"
                  "become a great and strong adventurer but the beastlies had other plans for them.\n"
                  "Rest well %s, maybe you will be reincarnated as a capable adventure."
                  % (self.name, self.enemy.name, self.name, self.name, self.name))
            tprint("You Died....")
            if self.hp == 0:
                answer = input("Would you like to reincarnate? y/n ")
                if answer == 'y' or answer == 'yes' or answer == 'Y' or answer == 'Yes':
                    main()
                    pass
                elif answer == 'n' or answer == 'no' or answer == 'N' or answer == 'No':
                    sys.exit()

    def use(self):
        if self.state != 'normal':
            print("Health potions can only be used outside of battle!")
            self.enemy_attacks()
        else:
            if self.pots > 0:
                answer = input("Do you want to use a potion? y/n: ")
                if answer == 'y' or answer == 'yes' or answer == 'Y' or answer == 'Yes':
                    if self.hp == self.hp_max:
                        print("%s health is full already." % self.name)
                    elif self.hp < self.hp_max:
                        self.pots = self.pots - 1
                        self.hp = self.hp_max
                        print("%s is fully healed from the health potion!" % self.name)
                elif answer == 'n' or answer == 'no' or answer == 'N' or answer == 'No':
                    return ()
                else:
                    print("That isn't a valid option.")
                    return ()
            if self.pots == 0:
                print("%s does not have any health potions to use." % self.name)
                return ()

    def addexp(self):
        earnedExp = self.exp + randint(0, 150)
        self.exp = self.exp + earnedExp
        print("%s has gained " % self.name + str(earnedExp) + " experience points!")

    def nextLvl(self):
        xpNeeded = self.lvl * 10
        if self.exp >= round((4 * (xpNeeded ** 3)) / 5):
            self.levelUp()

    def levelUp(self):
        self.hp = self.hp + 3
        self.hp_max = self.hp_max + 3
        self.lvl = self.lvl + 1
        self.base_evade = self.base_evade + 3
        self.base_evade_max = self.base_evade_max + 3
        self.base_attack = self.base_attack + 1
        print("Through slaying enemies as they get in the way of %s's exploring %s has\n"
              "gained more experience and \033[1;32;1mleveled up!\033[1;37;1m %s gained three\n"
              "additional health points, three additional evade points, and one attack point!"
              % (self.name, self.name, self.name,))

    def addInventory(self):
        self.inventory.append(Item)
        print('Added ' + Item + ' to bag.')

    def inventory(self):
        if self.state != 'normal':
            print("Inventory can only be used outside of battle!")
            self.enemy_attacks()
        elif self.inventory != "None" or self.inventory != "none":
            print("What do you want to check?")
            print("1.) Equipment")
            print("2.) Crafting")
            print("3.) Treasures")
            answer = input(" ")
            if answer == '1':
                print('peering into your bag you see the following:')
                for x, y in enumerate(self.inventory):
                    print(x, y)


Commands = {
    'save': Player.save,
    'quit': Player.quit,
    'help': Player.help,
    'status': Player.status,
    'rest': Player.rest,
    'explore': Player.explore,
    'flee': Player.flee,
    'attack': Player.attack,
    'use': Player.use,
    'inv': Player.inventory,
}


def load_game():
    load_name = input("Please enter save file name: ")
    load_path = ('saves/' + load_name + '.json')
    validcheck = os.path.isfile(load_path)
    if validcheck:
        print('System: Loading ' + load_path)
        with open(load_path, 'r') as f:
            j = json.load(f)
            Character.name = str(j['name'])
            Character.lvl = int(j['lvl'])
            Character.hp = int(j['hp'])
            Character.hp_max = int(j['hp_max'])
            Character.base_attack = int(j['base_atk'])
            Character.base_def = int(j['base_def'])
            Character.base_def_max = int(j['base_def_max'])
            Character.base_evade = int(j['base_evade'])
            Character.base_evade_max = int(j['base_evade_max'])
            Character.weap = str(j['curweap'])
            Character.gold = int(j['gold'])
            Character.gold_max = int(j['gold_max'])
            Character.pots = int(j['pots'])
            Player.exp = int(j['exp'])

    else:
        print('Invalid save name!')
        main()


def main():
    tprint("The Tower ")
    print('--------------------------------------------------------')
    print('---------- A Text-Based RPG by Ron and Ben. ------------')
    print('--------------------------------------------------------')
    print("1.) Start")
    print("2.) Continue")
    print("3.) Exit")
    options = input(">> ")

    if options == "1":
        hero = Player()
        hero.name = input("Hello adventurer, what do they call you? ")
        print("%s well met! Please choose your starting weapon." % hero.name)
        print("Your choices are the 1.) Rusty Sword, the 2.) Rusty Dagger, or the 3.) Wooden Bow")
        print("(Each weapon has different stats.")
        weapchoice = input("Please choose your weapon: ")
        introData = (csv.reader(open('data/intro.csv', 'r')))
        introDataClean = list(introData)
        introRoll = random.choice(introDataClean)
        if hero.curweap == "none":
            if weapchoice == "1":
                hero.curweap = "Rusty Sword"
                hero.base_attack = 13
                hero.base_evade_max = 8
                hero.base_evade = hero.base_evade_max
            if weapchoice == "2":
                hero.curweap = "Rusty Dagger"
                hero.base_attack = 9
                hero.base_evade_max = 11
                hero.base_evade = hero.base_evade_max
            if weapchoice == "3":
                hero.curweap = "Wooden Bow"
                hero.base_attack = 5
                hero.base_evade_max = 15
                hero.base_evade = hero.base_evade_max

            print("(Type 'help' to get a list of usable commands)\n")

            print("%s your adventure begins here, whether you live or die is up to the fates themselves\n"
                  "and a bit of skill on your behalf. I am your guide 'Aldos' and I will follow you\n"
                  "throughout your adventures, however, I will not interfere with the choices you make.\n"
                  % hero.name)

            print(str(introRoll).format(h = hero.name))
            pass

        else:
            print("No valid choice was made, you will go into your adventure with your bare hands.\n")
            hero.curweap = "Fist"
            hero.base_attack = 2
            hero.base_evade_max = 20
            hero.base_evade = hero.base_evade_max
            print("(Type 'help' to get a list of usable commands)\n")
            print("%s your adventure begins here, whether you live or die is up to the fates themselves\n"
                  "and a bit of skill on your behalf. I am your guide 'Aldos' and I will follow you\n"
                  "throughout your adventures, however, I will not interfere with the choices you make.\n"
                  % hero.name)
            print("Equipped with their satchel and trusty dagger passed down their bloodline to each\n"
                  "adventurer %s kisses their mother on the cheek and rushes out the front door towards\n"
                  "the 'Cave of Beastlies'. Coming to the entrance of the cave %s takes a deep breath\n"
                  "and pushes forward." % (hero.name, hero.name))
            pass

    elif options == "2":
        load_game()
        hero = Player()
        hero.name = Character.name
        hero.lvl = Character.lvl
        hero.gold = Character.gold
        hero.hp = Character.hp
        hero.hp_max = Character.hp_max
        hero.base_attack = Character.base_attack
        hero.base_def = Character.base_def
        hero.base_def_max = Character.base_def_max
        hero.base_evade = Character.base_evade
        hero.base_evade_max = Character.base_evade_max
        hero.curweap = Character.weap
        hero.exp = Player.exp
        hero.pots = Character.pots
        print('Welcome back ' + hero.name + ', ' + 'time to continue your adventure!')
        print("Enter your next command(if you need a refresher, type 'help')")
        # print('debug:' + str(hero.lvl) + str(hero.gold) + str(hero.hp) + str(hero.hp_max) + str(hero.base_attack)
        # + str(hero.base_def) + str(hero.base_def_max) + str(hero.base_evade) + str(hero.base_evade_max)
        # + str(hero.weap) + str(hero.pots))

    elif options == "3":
        sys.exit()

    while hero.hp > 0:
        line = input(">> ")
        args = line.split()
        if len(args) > 0:
            commandFound = False
            for c in Commands.keys():
                if args[0] == c[:len(args[0])]:
                    Commands[c](hero)
                    commandFound = True
                    break
            if not commandFound:
                print("%s is confused about the choice made..." % hero.name)


if __name__ == '__main__':
    main()