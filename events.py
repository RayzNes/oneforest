import random

def handle_random_event(player):
    event = random.choice(["медведь", "волк", "заблудился"])
    if event == "медведь":
        player.health -= 30
    elif event == "волк":
        player.health -= 20
        if random.random() < 0.3:
            player.inventory["мех"] += 1
    elif event == "заблудился":
        player.thirst -= 10
        player.hunger -= 10
        player.warmth -= 10