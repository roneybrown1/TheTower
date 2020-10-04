from art import *
import sys
import os
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
        self.weap = ["Sword", "Dagger", "Bow", "Fist"]
        self.weapons = ['Rapier', 'Sabre', 'Cutlass', 'Scimitar', 'Long Sword', 'Bastard Sword', 'Great Sword']
        self.curweap = 'none'
        self.inventory = 'none'

    def do_damage(self, enemy):
        damage = min(max(randint(0, self.base_attack) - randint(0, enemy.hp), 0),
                     enemy.hp, self.base_def, self.base_evade)
        enemy.hp = enemy.hp - damage
        if damage == 0:
            print("%s was able to evade %s's \033[1;31;1mattack\033[1;37;1m." % (enemy.name, self.name))
            print("\033[1;31;1m""0 damage""\033[1;37;1m taken.")
        else:
            print("%s landed a \033[1;31;1mdamaging\033[1;37;1m blow on the %s,"
                  % (self.name, enemy.name))
            print("\033[1;31;1m" + str(damage) + "\033[1;31;1m", "\033[1;37;1mdamage was dealt!")
            return enemy.hp <= 0



class Enemy(Character):
    def __init__(self, player):
        Character.__init__(self)
        first = ("giant", "fire-eyed", "half-dead", "rotting", "bloated", "hulking", "grizzly", "angered", "injured",
                 "erratic", "frenzied", "yellow", "red", "black", "wasting", "gross", "ghastly", "demonic", "doomed",
                 "savage", "stone", "elemental", "abyssal", "plague", "behemoth", "gelatinous", "zombie", "oozing",
                 "lesser", "fabled", "fiendish", "possessed")
        second = ("goblin", "warlock", "witch", "minotaur", "kobald", "skeleton", "ogre", "rat", "spirit", "troll",
                  "vampire", "banshee", "warrior", "dog", "spider", "snake", "harpy", "specter", "dwarf", "hobgoblin",
                  "bat", "familiar", "golem", "thief", "orc", "halfling", "drow", "pixie", "satyr", "imp", "hag",
                  "lich", "crawler", "wasp", "mage")
        titleOne = random.choice(first)
        titleTwo = random.choice(second)
        self.name = (titleOne + " " + titleTwo)
        self.hp = random.randint(1, player.hp)
        self.base_attack = 15
        self.base_def = 10
        self.base_evade = 10


class Player(Character):
    def __init__(self):
        Character.__init__(self)
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
        self.weap = {}
        self.curweap = "none"
        self.inventory = ["none"]

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
                    'savename': save_name, 'name':self.name, 'lvl': self.lvl, 'hp': self.hp, 'hp_max':self.hp_max,
                    'base_atk':self.base_attack, 'base_def':self.base_def, 'base_def_max':self.base_def_max, 'base_evade':self.base_evade,
                    'base_evade_max':self.base_evade_max, 'curweap':self.curweap,'gold':self.gold,'gold_max':self.gold_max,'pots':self.pots
                }
                with open(path, 'w+') as f:
                    json.dump(data, f)
                print ('DEBUG: Saved ' + save_name + ' in ' + path)
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
        print("%s's current stats are...\n Level: %s\n Health: %d/%d\n Attack: %s\n "
              "Def: %d/%d\n Evade: %d/%d\n Weapon: %s\n Gold: %d/%d\n Potions: %s"
              % (self.name, self.lvl, self.hp, self.hp_max, self.base_attack,
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
            if random.randint(0, 100) > 95:
                print("%s sees an opening in the cave wall, there is a faint glimmer in the distance\n"
                      % self.name)
                explore = input("Explore the opening? y/n: ")
                if explore == 'y':
                    if random.randint(0, 30) > 15:
                        print("%s moves through the opening and towards the glimmer, moving closer %s and see\n"
                              "a treasure chest covered in strange symbols." % (self.name, self.name))
                        open = input("Do you want to open the chest? y/n: ")
                        if open == 'y':
                            print("%s slowly opens the chest, as they do they reveal " % self.name)
                            if random.randint(0, 50) > 25:
                                if random.randint(0, 20) > 10:
                                    print("a shimmering %s" % random.choices(self.weapons))
                                    random.choice(self.weapons)
                                    equip = input("Do you want to equip the item? y/n: ")
                                    if equip == 'y':
                                        self.curweap = random.choice(self.weapons)
                                    elif equip == 'n':
                                        print("The item has been added to your inventory.")
                                        self.inventory = self.weap
                                elif random.randint(0, 20) < 10:
                                    print("25 gold pieces!")
                                    self.gold = self.gold + 25
                                else:
                                    print("The chest was empty, someone or something must have\n"
                                          "gotten here first. %s continues exploring the cave" % self.name)
                        elif open == 'n':
                            print("%s decides to not open the chest and continue exploring." % self.name)

        if random.randint(0, 1):
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
                if random.randint(0, self.hp) < 10:
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
                print(self.weap)
                print("Do you want to equip an item?")
                print("1.) Weapon")
                print("2.) Armor")
                answer = input(" ")
                if answer == '1':
                    print(self.weap)


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
        print('DEBUG: Loading ' + load_path)
        with open(load_path, 'r') as f:
            j = json.load(f)
            Character.name = str(j['name'])
            Character.lvl = str(j['lvl'])
            Character.hp = str(j['hp'])
            Character.hp_max = str(j['hp_max'])
            Character.base_attack = str(j['base_atk'])
            Character.base_def = str(j['base_def'])
            Character.base_def_max = str(j['base_def_max'])
            Character.base_evade = str(j['base_evade'])
            Character.base_evade_max = str(j['base_evade_max'])
            Character.weap = str(j['curweap'])
            Character.gold = str(j['gold'])
            Character.gold_max = str(j['gold_max'])
            Character.pots = str(j['pots'])

    else:
        print('Debug: Invalid save name!')
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
        pass
    elif options == "2":
        load_game()
        print ('Welcome back ' + Character.name + '!')


    elif options == "3":
        sys.exit()


if __name__ == '__main__':
    main()

p = Player() # P ISSUE HERE PERHAPS?
p.name = input("Hello adventurer, what do they call you? ")
print("%s well met! Choose your starting weapon." % p.name)
print("Choose between the 1.) Sword, 2.) Dagger, or 3.) Bow")
weapchoice = input("Choose your weapon: ")
if p.curweap == "none":
    if weapchoice == "1":
        p.curweap = "Sword"
        p.base_attack = 13
        p.base_evade_max = 8
        p.base_evade = p.base_evade_max
    if weapchoice == "2":
        p.curweap = "Dagger"
        p.base_attack = 9
        p.base_evade_max = 11
        p.base_evade = p.base_evade_max
    if weapchoice == "3":
        p.curweap = "Bow"
        p.base_attack = 5
        p.base_evade_max = 15
        p.base_evade = p.base_evade_max
else:
    print("No valid choice was made, you will go in with your bare hands.")
    p.curweap = "Fist"
    p.base_attack = 2
    p.base_evade_max = 20
    p.base_evade = p.base_evade_max

print("(Type 'help' to get a list of usable commands)\n")
print("%s your adventure begins here, whether you live or die is up to the fates themselves\n"
      "and a bit of skill on your behalf. I am your guide 'Aldos' and I will follow you\n"
      "throughout your adventures, however, I will not interfere with the choices you make.\n"
      % p.name)
print("Equipped with their satchel and trusty dagger passed down their bloodline to each\n"
      "adventurer %s kisses their mother on the cheek and rushes out the front door towards\n"
      "the 'Cave of Beastlies'. Coming to the entrance of the cave %s takes a deep breath\n"
      "and pushes forward." % (p.name, p.name))

while p.hp > 0:
    line = input(">> ")
    args = line.split()
    if len(args) > 0:
        commandFound = False
        for c in Commands.keys():
            if args[0] == c[:len(args[0])]:
                Commands[c](p)
                commandFound = True
                break
        if not commandFound:
            print("%s is confused about the choice made..." % p.name)


