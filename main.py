
def main():
    pass


if __name__ == '__main__':
    main()

from random import randint


class Character:
    def __int__(self):
        self.name = ""
        self.hp = 1
        self.hp_max = 1

    def do_damage(self, enemy):
        damage = min(max(randint(0, self.hp) - randint(0, enemy.hp), 0), enemy.hp)
        enemy.hp = enemy.hp - damage
        if damage == 0:
            print("%s was able to evade %s attack.") % (enemy.name, self.name)
        else:
            print("%s landed a blow on %s with a swing of their dagger.")
            return enemy.hp <= 0


class Enemy(Character):
    def __init__(self, player):
        Character.__init__(self)
        self.name = ['a goblin', 'a giant spider', 'a rotting skeleton', 'a half-dead wizard']
        self.hp = randint(1, player.hp)


class Player(Character):
    def __init__(self):
        Character.__init__(self)
        self.state = 'normal'
        self.hp = 25
        self.hp_max = 25

    def quit(self):
        print("%s could not handle the stress of being alone, they sat behind a rock pulling their knees to their "
              "chest, closed their eyes and faded away into nothingness... Sleep well sweet %s, "
              "you tried your hardest...") % self.name
        self.hp = 0

    def help(self):
        print (Commands.keys())

    def status(self):
        print("%s's current stats are...: %d%d") % (self.name, self.state, self.hp, self.hp_max)

    def tired(self):
        print("%s can feel themselves getting weaker, one hp lost. You are tired and needs to rest.") % self.name
        self.hp = max(1, self.hp - 1)

    def rest(self):
        if self.state != 'normal':
            print("%s cannot rest at this time!") % self.name
            self.enemy_attacks()
        else:
            print("%s finds a place to settle, they brush any dirt and debris away."
                  "Taking their satchel using it as a pillow, %s drift off to sleep. %s is refreshed, "
                  "gain one hp") % self.name
            self.hp = self.hp + 1
        if randint(0, 1):
            self.enemy = Enemy(self)
            print("A quick scuttle of feet/legs awakens %s from their sleep, before they can react they are attacked "
                  "by %s") % (self.name, self.enemy.name)
            self.state = 'fight'
            self.enemy_attacks()
        else:
            if self.hp < self.hp_max:
                self.hp = self.hp + 1
            else:
                print("%s has overslept causing them to feel drowsy, one hp lost.") % self.name
                self.hp = self.hp - 1

    def explore(self):
        if self.state != 'normal':
            print("Are you insane?! %s is being attack and cannot continue exploring... FOCUS! If you are not "
                  "ready to take on this beastlie, 'flee'.") % self.name
            self.enemy_attacks()
        else:
            print("%s moves cautiously through the twisting and turning tunnels of the cave, with each step the cave "
                  "seems to be alive and changing. %s continues forward.") % self.name
        if randint(0, 1):
            self.enemy = Enemy(self)
            print(" As %s moves through the cave they notice a scuttling sound coming from behind them. "
                  "Oh no! %s has been attacked by %s") % (self.name, self.enemy.name)
            self.state = 'fight'
        else:
            if randint(0, 1):
                self.tired()

    def flee(self):
        if self.state != 'fight':
            print("Oh....Okay...There is nothing to flee from, but I won't stop you %s...") % self.name
            self.tired()
        else:
            if randint(1, self.hp + 5) > randint(1, self.enemy.hp):
                print()




Commands = {
    'quit': Player.quit,
    'help': Player.help,
    'status': Player.status,
    'rest': Player.rest,
    'explore': Player.explore,
    'flee': Player.flee,
    'attack': Player.attack,
}

p = Player()
p.name = input("Hello adventurer, what do they call you? ")
print("(Type 'help' to get a list of usable commands)\n")
print("%s your adventure begins here, whether you live or die is up to the fates themselves and a bit of skill on your "
      "behalf. I am your guide 'Aldos' and I will follow you throughout your adventures, however, I will not interfere"
      "with the choices you make. \n") % p.name
print(" Equipped with their satchel and trusty dagger passed down their bloodline to each adventurer %s kisses their "
      "mother on the cheek and rushes out the front door towards the 'Cave of Beastlies'. Coming to the entrance of "
      "the cave %s takes a deep breath and pushes forward.") % p.name

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
                print("%s is confused about the choice made") % p.name
