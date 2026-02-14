import time
import random
import json
class colors:
    black='\033[30m'
    red='\033[31m'
    green='\033[32m'
    orange='\033[33m'
    blue='\033[34m'
    purple='\033[35m'
    cyan='\033[36m'
    lightgrey='\033[37m'
    darkgrey='\033[90m'
    lightred='\033[91m'
    lightgreen='\033[92m'
    yellow='\033[93m'
    lightblue='\033[94m'
    pink='\033[95m'
    lightcyan='\033[96m'
    end="\033[0m"

class text:
    def __init__(self):
        pass
    def strike(self, weaponType, enemy):
        if weaponType == "blade":
            if enemy:
                return random.choice(["swings", "swipes", "slashes", "slices"])
            else:
                return random.choice(["swing", "swipe", "slash", "slice"])
        elif weaponType == "firearm":
            if enemy:
                return random.choice(["shoots", "fires", "blasts"])
            else:
                return random.choice(["shoot", "fire", "blast"])
    def move(self):
        return random.choice(["enter", "walk into", "move to"])
    def obtain(self):
        return random.choice(["grab", "collect", "claim", "obtain", "take", "get"])
    def insult(self):
        setup = ["your mother looks like", "you look like", "you are", "you smell like", "you arent even", "you feel like", "your family is", "your father is", "your brother is", "your sister is", "your built like"]
        punchLine = ["a dumb person", "a retard", "a fish", "a camel", "a donkey", "a grandma", "stupid", "bad", "your mother", "a gay chicken", "gay chicken"]
        return f" {random.choice(setup)} {random.choice(punchLine)}"
t = text()
vowls = ["a", "e", "i", "o", "u"]
helpText = "help : explains commands in detail 'help'\ninspect : inspects your surroundings 'inspect'\ncheck : checks infomation about an NPC or yourself 'check [npc name]', 'check'\ntalk : talk to an NPC in the same room 'talk [npc name]', 'talk to [npc name]'\ngrab: obtains and item in the same room 'grab [item name]'\nuse: uses an item in your inventory 'use [item name]'\nfight/attack: battles an NPC in the same room 'fight [npc name]', 'attack [npc name]'\nenter/move: enters a location connected to yours 'enter [location name]', 'move to [location name]'"

def say(text, speed=0.03, newLine=True, color=None):
    text = str(text)
    for i in range(len(text)):
        if color == None:
            print(text[i],end="")
        else:
            print(f"{color}{text[i]}{colors.end}", end="")
        time.sleep(speed)
    if newLine:
        print("")

class statHolder:
    def __init__(self, strength, endurance, speed, inteligence, dexterity, ambition):
        self.strength = strength
        self.endurance = endurance
        self.speed = speed
        self.inteligence = inteligence
        self.dexterity = dexterity
        self.ambition = ambition
    
class NPC:
    def __init__(self, name, description, speech, hostility, inventory, stats, myLocation):
        self.name = name
        self.description = description
        self.speech = speech
        self.hostility = hostility
        self.inventory = inventory
        self.stats = stats
        self.myLocation = myLocation
        self.tempHostility = hostility
    def talk(self):
        say(", ".join(self.speech.keys()), 0.03, False)
        say(" or nevermind")
        answer = None
        while answer not in self.speech:
            answer = input("[you]> ").lower()
            if answer == "nevermind":
                return
        options = self.speech[answer]
        index = int((self.tempHostility / 100) * len(options))
        index = min(index, len(options) - 1)

        self._handle_dialog(options[index], answer)

    def _handle_dialog(self, line, responce):
        if isinstance(line, list):
            prompt, responses = line
            say(prompt)
            say(", ".join(responses), 0.03, False)
            say(" or nevermind")
            user_input = None
            while user_input not in responses:
                user_input = input("[you]> ").lower()
                if user_input == "nevermind":
                    return
            self.speechEffects(user_input)
            self._handle_dialog(responses[user_input], user_input)
        else:
            self.speechEffects(responce)
            say(f"[{self.name}] {line}")
            self.talk()
    def speechEffects(self, speech):
        if speech == "insult":
            self.insult()
    def check(self):
        say(self.name, color=colors.yellow)
        say(" Strength", newLine=False, color=colors.red)
        say(f" - {self.stats.strength}")
        say(" Endurance", newLine=False, color=colors.lightgrey)
        say(f" - {self.stats.endurance}")
        say(" Speed", newLine=False, color=colors.lightblue)
        say(f" - {self.stats.speed}")
        say(" Inteligence", newLine=False, color=colors.blue)
        say(f" - {self.stats.inteligence}")
        say(" Dexterity", newLine=False, color=colors.darkgrey)
        say(f" - {self.stats.dexterity}")
        say(" Ambition", newLine=False, color=colors.orange)
        say(f" - {self.stats.ambition}")
        say(self.description)
        say(f"\nhostility towards you: {self.hostility}")
    def insult(self):
        say(f"[you]{t.insult()}")
class item:
    def __init__(self, name, description, myLocation, rarity):
        self.name = name
        self.description = description
        self.myLocation = myLocation
        self.rarity = rarity
    def check(self):
        say(self.name, color=self.col())
        say(self.description)
    def col(self):
        if self.rarity == 1:
            return colors.darkgrey
        elif self.rarity == 2:
            return colors.lightcyan
        elif self.rarity == 3:
            return colors.yellow
        elif self.rarity == 4:
            return colors.purple
    def grab(self):
        say(f"You {t.obtain()} the ", newLine=False, speed=0.04)
        say(self.name, color=self.col(), speed=0.06)
        self.myLocation.items.remove(self)
        p.inventory.append(self)
    def use(self):
        self.check()
        say("you use the ", newLine=False)
        say(self.name, color=self.col())
    def useInFight(self):
        say("you use the ", newLine=False)
        say(self.name, color=self.col())
class weapon(item):
    def __init__(self, name, description, myLocation, rarity, damage, delay, critMuliplier, critChance, missChance, statusEffects, statusEffectsChance):
        super().__init__(name, description, myLocation, rarity)
        self.name = name
        self.description = description
        self.myLocation = myLocation
        self.rarity = rarity
        self.damage = damage
        self.delay = delay
        self.critMultiplier = critMuliplier
        self.critChance = critChance
        self.missChance = missChance
        self.statusEffects = statusEffects
        self.statusEffectsChance = statusEffectsChance
        self.delayTimer = 0
        self.isWeapon = True
    def getStatusEffects(self):
        effectsToGive = []
        for i in range(len(self.statusEffects)):
            if (random.randrange(0, 101) < self.statusEffectsChance[i]):
                effectsToGive.append(self.statusEffects[i][:])
        return effectsToGive
    def getDamage(self, userStats):
        damage = self.damage * ((userStats.strength / 100) + 1)
        if (random.randrange(0, 101) < (self.critChance * ((userStats.ambition / 100) + 1))):
            damage *= self.critMultiplier
        return damage
    def testMiss(self, userStats):
        if (random.randrange(0, 101) < (self.missChance * ((userStats.ambition / 200) + 1))):
            return True
        else:
            return False
    def check(self):
        say(self.name, color=self.col())
        say(" damage - ",newLine=False)
        say(self.damage, color=colors.red)
        say(" attack delay - ",newLine=False)
        say(self.delay, color=colors.orange)
        say("has a ",newLine=False)
        say(f"{self.critChance}%", color=colors.purple, newLine=False)
        say(" chance if inflicting ",newLine=False)
        say(f"{self.critMultiplier}x", color=colors.lightblue, newLine=False)
        say(" damage")
        for i in range(len(self.statusEffects)):
            say(f" has a {self.statusEffectsChance[i]}% chance of inflicting {self.statusEffects[i][0]} for {self.statusEffects[i][1]} turns")
        say("has a ", newLine=False)
        say(f"{self.missChance}%", color=colors.darkgrey, newLine=False)
        say(" chance of missing an attack")
class healthItem(item):
    def __init__(self, name, description, myLocation, rarity, healingFactor):
        super().__init__(name, description, myLocation, rarity)
        self.name = name
        self.description = description
        self.myLocation = myLocation
        self.rarity = rarity
        self.healingFactor = healingFactor
    
class location:
    def __init__(self, name, description, items, NPCs, connections):
        self.name = name
        self.description = description
        self.items = items
        self.NPCs = NPCs
        self.connections = connections
        self.entered = False
    def check(self):
        say(self.name)
        say(self.description)
    def checkSurroundings(self):
        if len(self.items) > 0:
            say(f"in {self.name} you can see" , newLine=False)
            index = 0
            for i in self.items:
                if index == len(self.items)-1 and index != 0:
                    say(" and", newLine=False)
                elif index != 0:
                    say(",",newLine=False)
                if i.name[0].lower() in vowls:
                    say(" an ",newLine=False)
                else:
                    say(" a ",newLine=False)
                say(i.name, newLine=False, color=i.col(), speed=0.05)
                index += 1
            say("")
        if len(self.NPCs) > 0:
            say("There is", newLine=False)
            index = 0
            for i in self.NPCs:
                if index == len(self.NPCs)-1 and index != 0:
                    say(" and", newLine=False)
                elif index != 0:
                    say(",",newLine=False)
                say(f" {i.name}", newLine=False, color=colors.yellow, speed=0.05)
                index += 1
            say("")
        if len(self.connections) > 0:
            say("You can enter:", newLine=False)
            index = 0
            for i in self.connections:
                if index == len(self.connections)-1 and index != 0:
                    say(" or", newLine=False)
                elif index != 0:
                    say(",",newLine=False)
                say(f" {i.name}", newLine=False, color=colors.yellow, speed=0.05)
                index += 1
            say("")
    def enter(self):
        say(f"you {t.move()} {self.name}")
        if self.entered == False:
            self.firstEnter()
            self.entered = True
    def firstEnter(self):
        pass
class fight:
    def __init__(self, enemy):
        self.enemy = enemy
        self.enemyHealth = 100
        self.statusEffects = []
        self.enemyStatusEffects = []
        self.playerWeapons = []
        self.playerDefending = False
        self.enemyDefending = False
        for i in p.inventory:
            if hasattr(i, "isWeapon"):
                self.playerWeapons.append([i,0])
        self.running = True
        say("you enter a fight with ", newLine=False)
        say(self.enemy.name, speed=0.05, color=colors.red)
        while self.running:
            self.drawStats()
            self.newTurn()
    def drawStats(self):
        say("You",speed=0.01,color=colors.blue,newLine=False)
        say(f"                        {self.enemy.name}",speed=0.01,color=colors.red)
        #player health bar
        healthBarLength = round(p.health / 10)
        if p.health > 66.6:
            col = colors.green
        elif p.health > 33.3:
            col = colors.yellow
        else:
            col = colors.red
        for i in range(healthBarLength):
            say("█",newLine=False,color=col,speed=0.01)
        for i in range(10-healthBarLength):
            say("█",newLine=False,color=colors.black,speed=0.01)
        say(p.health, newLine=False, color=col,speed=0.01)
        say("/100", speed=0.01, newLine=False, color=colors.green)
        say("          ",0.01, False)
        #enemy health bar
        healthBarLength = round(self.enemyHealth / 10)
        if self.enemyHealth > 66.6:
            col = colors.green
        elif self.enemyHealth > 33.3:
            col = colors.yellow
        else:
            col = colors.red
        for i in range(healthBarLength):
            say("█",newLine=False,color=col,speed=0.01)
        for i in range(10-healthBarLength):
            say("█",newLine=False,color=colors.black,speed=0.01)
        say(self.enemyHealth, newLine=False, color=col,speed=0.01)
        say("/100", speed=0.01, color=colors.green)

    def damageEnemy(self, ammount, cause):
        ammount = ammount / ((self.enemy.stats.endurance / 100) + 1)
        ammount = round(ammount)
        say(f"{cause} deals ", newLine=False)
        say(ammount, newLine=False, color = colors.yellow, speed=0.06)
        say(f" damage to {self.enemy.name}")
        self.enemyHealth -= ammount
        if self.enemyHealth <= 0:
            self.playerWin()

    def damagePlayer(self, ammount, cause):
        ammount = ammount / ((p.stats.endurance / 100) + 1)
        ammount = round(ammount)
        say(f"{cause} deals you ", newLine=False)
        say(ammount, newLine=False, speed=0.06, color=colors.red)
        say(" damage")
        p.health -= ammount
        if p.health <= 0:
            self.enemyWin()

    def playerWin(self):
        say("YOU WIN", color=colors.lightgreen, speed=0.1)
        self.running = False
    def enemyWin(self):
        say("YOU LOST", color = colors.red, speed=0.1)
        self.running = False

    def newTurn(self):
        time.sleep(0.4)
        if self.running:
            self.playerTurn()
        time.sleep(0.4)
        if self.running:
            self.enemyTurn()
        time.sleep(0.4)
        if self.running:
            index = 0
            for effect in self.enemyStatusEffects:
                if (effect[0] == "poison"):
                    self.damageEnemy(7, "poison")
                elif (effect[0] == "bleeding"):
                    self.damageEnemy(4, "bleeding")
                effect[1] -= 1
                if effect[1] <= 0:
                    self.enemyStatusEffects.pop(index)
                index += 1
            index = 0
            for effect in self.statusEffects:
                if (effect[0] == "poison"):
                    self.damagePlayer(7, "poison")
                elif (effect[0] == "bleeding"):
                    self.damagePlayer(4, "bleeding")
                effect[1] -= 1
                if effect[1] <= 0:
                    self.statusEffects.pop(index)
                index += 1
            for i in self.playerWeapons:
                if i[1] > 0:
                    i[1] -= 1

    def playerTurn(self):
        moves = ["attack", "use", "run", "defend"]
        move = None
        say("attack, use or run")
        while not move in moves:
            move = input(">")
        print("\033[H\033[J", end="")
        
        if move == "run":
            say("You run from ", newLine=False)
            say(self.enemy.name, color=colors.red)
            self.running = False
        elif move == "attack":
            say("Choose the weapon: ")
            for i in self.playerWeapons:
                say(f" -{i[0].name}", color=i[0].col(), newLine=False)
                if i[1] != 0:
                    say(f" ({i[1]})")
                else:
                    say("")
            foundWeapon = False
            while not foundWeapon:
                chosenWeapon = input(">").lower()
                for i in self.playerWeapons:
                    if i[0].name == chosenWeapon and i[1] <= 0:
                        chosenWeapon = i[0]
                        i[1] = i[0].delay
                        foundWeapon = True
                        break
                if not foundWeapon:
                    say(f"cannot use {chosenWeapon} at this time")
            if chosenWeapon.testMiss(p.stats):
                say(f"You swing your {chosenWeapon.name}")
                time.sleep(1)
                say("You miss")
            else:
                say(f"You swing your {chosenWeapon.name}")
                time.sleep(1)
                self.damageEnemy(chosenWeapon.getDamage(p.stats), chosenWeapon.name)
                if self.running == False:
                    return
                getStatusEffects = chosenWeapon.getStatusEffects()
                foundEffect = False
                for i in getStatusEffects:
                    for e in range(len(self.enemyStatusEffects)):
                        if i[0] == self.enemyStatusEffects[e][0]:
                            self.enemyStatusEffects[e] = i
                            foundEffect = True
                            break
                    if not foundEffect:
                        self.enemyStatusEffects.append(i)
                    say(f"You inflict {i[0]} onto {self.enemy.name} for {i[1]} turns")
        elif move == "use":
            foundItem = False
            say("what item:")
            for i in p.inventory:
                if not hasattr(i, "isWeapon"):
                    say(f" -{i.name}", color=i.col())
            while not foundItem:
                answer = input(">")
                index = 0
                for i in p.inventory:
                    if answer == i.name and not hasattr(i, "isWeapon"):
                        answer = i
                        foundItem = True
                        break
                    index += 1
                if not foundItem:
                    say(f"you cannot use {answer}")
            i.useInFight()
            time.sleep(0.4)
            if hasattr(i, "healingFactor"):
                say("you heal ", newLine=False)
                say(i.healingFactor, color=colors.lightgreen, newLine=False)
                say(" health")
                p.health += i.healingFactor
                p.health = min(100, p.health)
            p.inventory.pop(index)
            
    def enemyTurn(self):
        if self.enemy.hostility * random.uniform(0.9, 1.1) < 20:
            say(f"[{self.enemy.name}]I wont fight you, press run")
            return
        needToHeal = ((p.health - self.enemyHealth) * (len(self.enemyStatusEffects)+1)) + (100-self.enemyHealth)
        needToAttack = (self.enemy.hostility + (100 - p.health)) * ((self.enemy.stats.ambition / 100) + 1)

        needToHeal *= random.uniform(0.6, 1.4)
        needToAttack *= random.uniform(0.6, 1.4)

        random.shuffle(self.enemy.inventory)
        actions = sorted([needToAttack, needToHeal])
        if actions[-1] == needToHeal:
            for i in self.enemy.inventory:
                if hasattr(i, "healingFactor"):
                    say(f"{self.enemy.name} uses ", newLine=False)
                    say(i.name, color=i.col())
                    time.sleep(0.4)
                    say(f"{self.enemy.name} heals ", newLine=False)
                    say(i.healingFactor, color=colors.lightgreen, newLine=False)
                    say(" health")
                    self.enemyHealth += i.healingFactor
                    self.enemyHealth = min(100, self.enemyHealth)
                    break
        elif actions[-1] == needToAttack:
            for i in self.enemy.inventory:
                if hasattr(i, "isWeapon"):
                    chosenWeapon = i
                    break
            if chosenWeapon.testMiss(self.enemy.stats):
                say(f"{self.enemy.name} {t.strike("blade", True)} their {chosenWeapon.name} but misses")
            else:
                say(f"{self.enemy.name} {t.strike("blade", True)} their {chosenWeapon.name}")
                self.damagePlayer(chosenWeapon.getDamage(self.enemy.stats), chosenWeapon.name)
                if self.running == False:
                    return
                getStatusEffects = chosenWeapon.getStatusEffects()
                foundEffect = False
                for i in getStatusEffects:
                    for e in range(len(self.statusEffects)):
                        if i[0] == self.statusEffects[e][0]:
                            self.statusEffects[e] = i
                            foundEffect = True
                            break
                    if not foundEffect:
                        self.statusEffects.append(i)
                    say(f"He inflicts {i[0]} onto you for {i[1]} turns")
class player:
    def __init__(self, inventory, location, armour, stats):
        self.inventory = inventory
        self.location = location
        self.armour = armour
        self.stats = stats
        self.maxHealth = 100
        self.health = self.maxHealth
    def command(self):
        allowedCommands = ["check", "attack", "inspect", "grab", "talk", "move", "help", "enter", "fight", "use"]
        answer = "None"
        while not answer.split()[0] in allowedCommands:
            answer = input(">").lower()
        print("\033[H\033[J", end="")
        if " " in answer:
            answer = answer.split()
            if answer[0] == "check":
                foundNPC = False
                for i in self.location.NPCs:
                    if i.name == answer[1]:
                        i.check()
                        foundNPC = True
                        break
                if not foundNPC:
                    say(f"No one named ",newLine=False)
                    say(answer[1],color=colors.yellow)
            elif answer[0] == "grab":
                foundItem = False
                for i in self.location.items:
                    if i.name == answer[1]:
                        i.grab()
                        foundItem = True
                        break
                if not foundItem:
                    say(f"You cannot find ",newLine=False)
                    say(answer[1],color=colors.yellow)
            elif answer[0] == "talk":
                if answer[1] == "to":
                    answer.pop(1)
                foundNPC = False
                for i in self.location.NPCs:
                    if i.name == answer[1]:
                        i.talk()
                        foundNPC = True
                        break
                if not foundNPC:
                    say(f"No one named ",newLine=False)
                    say(answer[1],color=colors.yellow)
            elif answer[0] == "move" or answer[0] == "enter":
                if answer[1] == "to":
                    answer.pop(1)
                foundLocation = False
                for i in self.location.connections:
                    if i.name == answer[1]:
                        self.location = i
                        i.enter()
                        foundLocation = True
                        break
                if not foundLocation:
                    say(f"You fail to enter ",newLine=False)
                    say(answer[1],color=colors.cyan)
            elif answer[0] == "attack" or answer[0] == "fight":
                foundNPC = False
                for i in self.location.NPCs:
                    if i.name == answer[1]:
                        fight(i)
                        foundNPC = True
                        break
                if not foundNPC:
                    say(f"No one named ",newLine=False)
                    say(answer[1],color=colors.yellow)
            elif answer[0] == "use":
                foundItem = False
                for i in self.inventory:
                    if i.name == answer[1]:
                        i.use()
                        foundItem = True
                        break
                if not foundItem:
                    say(f"There is no ",newLine=False)
                    say(answer[1],color=colors.yellow)
        else:
            if answer == "help":
                say(helpText, speed=0.02)
            elif answer == "check":
                self.check()
            elif answer == "inspect":
                self.location.checkSurroundings()
    def check(self):
        say("Your stats are:")
        say(" Strength", newLine=False, color=colors.red)
        say(f" - {self.stats.strength}")
        say(" Endurance", newLine=False, color=colors.lightgrey)
        say(f" - {self.stats.endurance}")
        say(" Speed", newLine=False, color=colors.lightblue)
        say(f" - {self.stats.speed}")
        say(" Inteligence", newLine=False, color=colors.blue)
        say(f" - {self.stats.inteligence}")
        say(" Dexterity", newLine=False, color=colors.darkgrey)
        say(f" - {self.stats.dexterity}")
        say(" Ambition", newLine=False, color=colors.orange)
        say(f" - {self.stats.ambition}")
        say("You have:", newLine=False)
        index = 0
        for i in self.inventory:
            if index == len(self.inventory)-1 and index != 0:
                say(" and", newLine=False)
            elif index != 0:
                say(",",newLine=False)
            if i.name[0].lower() in vowls:
                say(" an ",newLine=False)
            else:
                say(" a ",newLine=False)
            say(i.name, newLine=False, color=i.col(), speed=0.05)
            index += 1
        say("")

p = player([], None, [], statHolder(1, 1, 1, 1, 1, 1))