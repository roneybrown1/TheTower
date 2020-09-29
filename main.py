from art import *
import sys
import random
from random import randint


def main():
    tprint("The Tower ")
    print('--------------------------------------------------------')
    print('---------- A Text-Based RPG by Ron and Ben. ------------')
    print('--------------------------------------------------------')
    print("1.) Start")
    print("2.) Save")
    print("3.) Exit")
    options = input(">> ")

    if options == "1":
        pass
    elif options == "2":
        print("The save system is not yet implemented.")
        main()
    elif options == "3":
        sys.exit()


if __name__ == '__main__':
    main()



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
        self.curweap = 'none'

    def do_damage(self, enemy):
        damage = min(max(randint(0, self.base_attack) - randint(0, enemy.hp), 0),
                     enemy.hp, self.base_def, self.base_evade)
        enemy.hp = enemy.hp - damage
        if damage == 0:
            print("%s was able to evade %s's attack." % (enemy.name, self.name))
            print(" 0 damage taken.")
        else:
            print("%s landed a damaging blow on the %s,\n" % (self.name, enemy.name), damage, "damage was dealt!")
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
        self.weap = ["Sword", "Dagger", "Bow"]
        self.curweap = "none"

    def quit(self):
        print("%s could not handle the stress of being alone, they sat behind\n"
              "a rock pulling their knees to their chest, closed their eyes\n"
              "and faded away into nothingness... Sleep well sweet %s, you\n"
              "tried your hardest..." % (self.name, self.name))

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
                  "they can react they are attacked by a(n) %s." % (self.name, self.enemy.name))
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
                  "FOCUS! If you are not ready to take on this beastlie, you can 'flee'."
                  % (self.name, self.enemy.name))
            self.enemy_attacks()
        else:
            print("%s moves cautiously through the twisting and turning tunnels of the cave,\n"
                  "with each step the cave seems to be alive and changing. %s continues forward."
                  % (self.name, self.name))
        if random.randint(0, 1):
            self.enemy = Enemy(self)
            print("As %s moves through the cave they notice a scuttling sound coming from behind them.\n"
                  "Oh no! %s has been attacked by a(n) %s!" % (self.name, self.name, self.enemy.name))
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
                      "an escape route seeing an opening %s dashes towards the enemies blindside\n"
                      "and escaped into the darkness from the %s.\n" 
                      "(Careful, this action reduces defense.)"
                      % (self.name, self.name, self.enemy.name))
                self.base_def = self.base_def - 1
                self.enemy = None
                self.state = 'normal'
            else:
                print("%s couldn't escape from the %s and is forced to continue the battle.\n"
                      "You can try to flee again or attack the beastlie with your %s."
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
                print("%s readies themselves and with the right timing %s lands a killing blow on the %s!"
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
                          "gained more experience and leveled up! %s gained three additional health points,\n"
                          "three additional evade points, and one attack point!"
                          % (self.name, self.name, self.name,))
                    print(self.status())
                if random.randint(0, self.gold) < 10:
                    self.gold = self.gold + 5
                    print("%s found five gold pieces! Cha-ching!" % self.name)
                if random.randint(0, self.pots) < 5:
                    self.pots = self.pots + 1
                    print("%s found one health potion!" % self.name)
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
                    return()
                else:
                    print("That isn't a valid option.")
                    return()
            if self.pots == 0:
                print("%s does not have any health potions to use." % self.name)
                return()





Commands = {
    'quit': Player.quit,
    'help': Player.help,
    'status': Player.status,
    'rest': Player.rest,
    'explore': Player.explore,
    'flee': Player.flee,
    'attack': Player.attack,
    'use': Player.use,
}
p = Player()
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
