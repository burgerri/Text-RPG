"""https://github.com/JosephDelgadillo/python_text_rpg/blob/master/main.py"""
"""File added to GIT Repository Test"""
from classes.game import Persons, bcolors
from classes.magic import Spell
from classes.inventory import Item
import random

"""
print("\n")
print("NAME                     HP                                  MP")
print("                         _________________________           __________")
print(bcolors.BOLD + "Matul:     460/460      |" + bcolors.OKGREEN + "█████████████████████████" + bcolors.ENDC+ bcolors.BOLD + "|  65/65  |" + bcolors.OKBLUE + "██████████" + bcolors.ENDC + "|")
print("                         _________________________           __________")
print("Matul:     460/460      |█████████████████████████|  65/65  |██████████|")
print("                         _________________________           __________")
print("Matul:     460/460      |█████████████████████████|  65/65  |██████████|")
print("\n")"""

#  Create black magic
fire = Spell("Fire", 10, 100, "black")
thunder = Spell("Thunder", 10, 160, "black")
blizzard = Spell("Blizzard", 10, 160, "black")
meteor = Spell("Meteor", 20, 200, "black")
quake = Spell("Quake", 14, 140, "black")

#  Create white magic
cure = Spell("Cure", 12, 120, "white")
cura = Spell("Cura", 18, 200, "white")

# Create some Items
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Super Potion", "potion", "Heals 500 HP", 500)
elixer = Item("Elixer", "elixer", "Fully restores HP/MP of one party member", 999)
hielixer = Item("MegaElixer", "elixer", "Fully restores parties HP/MP", 999)

grenade = Item("Grenade", "attack", "Deals 500 damage", 500)



"""
magic = [{"name": "Fire", "cost": 10, "dmg": 160},
        {"name": "Thunder", "cost": 10, "dmg": 180},
        {"name": "Blizzard", "cost": 10, "dmg": 160}]
"""
#  Instantiate Player and Enemy
player_spells = [fire, thunder, blizzard, meteor, quake, cure, cura]
enemy_spells = [fire, meteor, cure]
player_items = [{"item": potion, "quantity": 15},
                {"item": hipotion, "quantity": 2},
                {"item": superpotion, "quantity": 2},
                {"item": elixer, "quantity": 3},
                {"item": hielixer, "quantity": 2},
                {"item": grenade, "quantity": 2}]
player1 = Persons("Matul :", 3260, 65, 300, 34, player_spells , player_items)
player2 = Persons("Angkol:", 4160, 65, 320, 34, player_spells , player_items)
player3 = Persons("Rangi :", 3089, 65, 250, 34, player_spells , player_items)

enemy1 = Persons("Imp   :", 1200, 130, 560, 325, enemy_spells, [])
enemy2 = Persons("Teraxx:", 19200, 80, 500, 25, enemy_spells, [])
enemy3 = Persons("Imp   :", 1200, 130, 560, 325, enemy_spells, [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

""" To test if damage functions are working
print("Physical dmg : ", player.generate_damage())
print("Physical dmg : ", player.generate_damage())
print("Physical dmg : ", player.generate_damage())
print("Magic dmg : {}".format(magic[0]["name"]),player.generate_spell_damage(0))
print("Magic dmg : {}".format(magic[1]["name"]),player.generate_spell_damage(1))
print("Magic dmg : {}".format(magic[2]["name"]),player.generate_spell_damage(2))
"""



running = True
i = 0

print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!!" + bcolors.ENDC)

while running:
    print("=========================================================================")
    print("NAME                      HP                                      MP")
    for player in players:
        player.get_stats()
    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:
        player.choose_action()
        choice = input("    Choose action : ")
        index = int(choice) - 1  # Required as the action index will start count from 0
        # print("You chose {}.".format(index))   # For error checking

        if index == 0:  # For non-magical attacks
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)  # Choose which enemy to attack
            enemies[enemy].take_damage(dmg)
            print("You attacked {} for {} points of damage.".format(enemies[enemy].name.replace(" ", "").replace(":", ""), dmg))

            if enemies[enemy].get_hp() == 0:  # If enemy is dead, then remove from enemies list
                print("{} has died".format(enemies[enemy].name.replace(" ", "").replace(":", "")))
                del enemies[enemy]

        elif index == 1:  # For magical attacks
            player.choose_magic()
            magic_choice = int(input("    Choose magic spell : ")) - 1

            if magic_choice == -1:
                continue

    #       magic_dmg = player.generate_spell_damage(magic_choice)
    #       spell = player.get_spell_name(magic_choice)
    #       cost = player.get_spell_mp_cost(magic_choice)

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()
            current_mp = player.get_mp()

            if spell.cost > current_mp:  # Test if sufficient mp to cast the get_spell_name
                print(bcolors.FAILD + "\nYou dont have enought MAGIC POINTS\n" + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == "white":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals for " + str(spell.dmg) + " HP" + bcolors.ENDC)
            elif spell.type == "black":
                enemy = player.choose_target(enemies)  # Choose which enemy to attack
                enemies[enemy].take_damage(magic_dmg)
                print(bcolors.OKBLUE + "\nYou attacked using the {} spell for {} points of MAGIC damage to {}.".format(spell.name, magic_dmg, enemies[enemy].name.replace(" ", "").replace(":", "")) + bcolors.ENDC)
                if enemies[enemy].get_hp() == 0:
                    print("{} has died".format(enemies[enemy].name.replace(" ","")))
                    del enemies[enemy]


        elif index == 2:
            player.choose_item()
            item_choice = int(input("    Choose item: ")) - 1

            if item_choice == -1:
                continue

            item = player.items[item_choice]["item"]

            if player.items[item_choice]["quantity"] == 0:  # Check for quantity of items left
                print(bcolors.FAIL + "None left...." + bcolors.ENDC)
                continue

            player.items[item_choice]["quantity"] -= 1  # to decrease the quantity of items after usage


            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + " heals for " + str(item.prop) + "HP" + bcolors.ENDC)
            elif item.type == "elixer":
                if item.name == "MegaElixer":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                print(bcolors.OKGREEN + "\n" + item.name + " fully restored your HP/MP " + bcolors.ENDC)
            elif item.type == "attack":
                enemy = player.choose_target(enemies)  # Choose which enemy to attack
                enemies[enemy].take_damage(item.prop)
                print(bcolors.FAIL + "\n" + item.name + " deals " + str(item.prop) + " points of damage to " + enemies[enemy].name.replace(" ","").replace(":", "") + bcolors.ENDC)
                if enemies[enemy].get_hp() == 0:
                    print("{} has died".format(enemies[enemy].name.replace(" ", "").replace(":", "")))
                    del enemies[enemy]

    # Check if Battle is over
    defeated_enemies = 0
    defeated_players = 0

    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1
    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1

    # Check if Player won
    if defeated_enemies == 2:
        print(bcolors.OKGREEN + "\nEnemy is DEAD, You WIN" + bcolors.ENDC)
        running = False
    # Check if Enemy won
    elif defeated_players == 2:
        print(bcolors.FAIL + "\nYou are DEAD, enemy has defeated you!!" + bcolors.ENDC)
        running = False

    # Enemy Attack Sequence
    for enemy in enemies:
        enemy_choice = random.randrange(0,2)  # To randomly select was action the enemy will perform

        if enemy_choice == 0:  # for when enemy chooses to attack
            target = random.randrange(0, 3)  # randomly select player target for enemy to attack
            enemy_dmg = enemy.generate_damage()  # Enemy attack sequence
            players[target].take_damage(enemy_dmg)  # targetting the array called players
            print("{} attacked {} for {} points of damage.".format(enemy.name.replace(" ", ""), players[target].name.replace(" ", "").replace(":", ""), enemy_dmg))
            if players[target].get_hp() == 0:
                print("{} has died".format(players[target].name.replace(" ","")))
                del players[player]

        elif enemy_choice == 1:
            spell, magic_dmg = enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)
            if spell.type == "white":
                enemy.heal(magic_dmg)
                print(bcolors.OKBLUE + spell.name + " heals {} for ".format(enemy.name.replace(" ", "")) + str(spell.dmg) + " HP" + bcolors.ENDC)
            elif spell.type == "black":
                target = random.randrange(0, 3)  # randomly select player target for enemy to attack
                players[target].take_damage(magic_dmg)
                print(bcolors.OKBLUE + "{} attacked using the {} spell for {} points of MAGIC damage to {}.".format(enemy.name.replace(" ",""), spell.name, magic_dmg, players[target].name.replace(" ", "").replace(":", "")) + bcolors.ENDC)
                if players[target].get_hp() == 0:
                    print("{} has died".format(players[target].name.replace(" ","")))
                    del players[player]
