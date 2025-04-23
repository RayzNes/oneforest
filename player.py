import random

class Player:
    def __init__(self):
        self.health = 100
        self.thirst = 100
        self.warmth = 100
        self.hunger = 100
        self.herbalism = 0
        self.foraging = 0
        self.medicine = 0
        self.season = "зима"
        self.day = 1
        self.inventory = {"ягоды": 0, "коренья": 0, "травы": 0, "палки": 0, "мех": 0, "еда": 0}
        self.has_fur_clothing = False
        self.is_sick = False
        self.days_without_sleep = 0

    def boil_water(self):
        self.thirst = min(100, self.thirst + 20)

    def rest(self):
        self.health = min(100, self.health + 10)

    def sleep(self):
        self.days_without_sleep = 0
        self.health = min(100, self.health + 15)

    def forage(self):
        self.foraging += 5
        self.herbalism += random.randint(0, 3)
        item = random.choice(["ягоды", "коренья", "травы", "палки"])
        self.inventory[item] += 1

    def hunt(self):
        if random.random() < 0.6:
            item = random.choice(["еда", "мех"])
            self.inventory[item] += 1
        else:
            self.health -= 10  # Риск ранения

    def eat(self):
        if self.inventory["еда"] > 0:
            self.inventory["еда"] -= 1
            self.hunger = min(100, self.hunger + 30)
        elif self.inventory["ягоды"] > 0:
            self.inventory["ягоды"] -= 1
            self.hunger = min(100, self.hunger + 10)

    def craft_warm_infusion(self):
        if self.inventory["травы"] >= 2:
            self.inventory["травы"] -= 2
            self.warmth = min(100, self.warmth + 20)

    def craft_medicine(self):
        if self.inventory["коренья"] >= 2:
            self.inventory["коренья"] -= 2
            self.is_sick = False
            self.health = min(100, self.health + 15)

    def craft_fur_clothing(self):
        if self.inventory["мех"] >= 3 and not self.has_fur_clothing:
            self.inventory["мех"] -= 3
            self.has_fur_clothing = True