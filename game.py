import pygame
import random
from player import Player
from interface import draw_interface
from events import handle_random_event
import asyncio

# Константы
WIDTH = 800
HEIGHT = 600
FPS = 30
FONT_SIZE = 20

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
BROWN = (139, 69, 19)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)

# Глобальные переменные (инициализируются в setup)
screen = None
clock = None
font = None
player = None

def setup():
    global screen, clock, font, player
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Один в лесу 2")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, FONT_SIZE)
    player = Player()

def update_loop():
    global player

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

    # Эффекты сезона
    if player.season == "зима":
        player.warmth -= 0.5 * (0.5 if player.has_fur_clothing else 1.0)
    elif player.season == "лето":
        player.warmth += 0.5
        player.thirst -= 0.3

    # Обновление состояния
    player.thirst -= 0.2
    player.hunger -= 0.15
    player.health -= 0.1 if player.warmth < 30 or player.thirst < 30 or player.hunger < 30 else 0
    if player.is_sick:
        player.health -= 0.2
    player.warmth = max(0, min(100, player.warmth))
    player.thirst = max(0, min(100, player.thirst))
    player.hunger = max(0, min(100, player.hunger))
    player.health = max(0, min(100, player.health))

    # Болезнь при низком тепле
    if player.warmth < 30 and random.random() < 0.01 and not player.is_sick:
        player.is_sick = True

    # Штраф за недосып
    if player.days_without_sleep >= 3:
        player.health -= 0.3
        player.thirst -= 0.3
        player.hunger -= 0.3

    # Смена дня и сезона
    if pygame.time.get_ticks() % 10000 < 100:  # Каждые 10 секунд новый день
        player.day += 1
        player.days_without_sleep += 1
        if player.day % 10 == 0:
            player.season = "лето" if player.season == "зима" else "зима"

    # Случайные события
    if random.random() < 0.005:
        handle_random_event(player)

    # Отрисовка
    screen.fill(BLACK)

    # Лес (деревья)
    for i in range(10):
        pygame.draw.rect(screen, BROWN, (i * 80 + 20, 50, 10, 50))
        pygame.draw.polygon(screen, GREEN, [(i * 80 + 15, 50), (i * 80 + 35, 50), (i * 80 + 25, 20)])

    # Снег или звезды
    for _ in range(50):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        pygame.draw.rect(screen, WHITE, (x, y, 2, 2))

    # Игрок
    pygame.draw.rect(screen, BROWN, (100, 300, 20, 40))
    pygame.draw.rect(screen, WHITE, (105, 305, 10, 10))

    # Костер
    pygame.draw.rect(screen, ORANGE, (150, 320, 20, 20))
    if 150 <= 100 <= 170 and 320 <= 300 <= 340:
        player.warmth += 0.1

    # Интерфейс
    draw_interface(screen, font, player, WIDTH, HEIGHT, CYAN, BROWN, WHITE)

    pygame.display.flip()
    return True

async def main():
    while player.health > 0:
        if not update_loop():
            break
        await asyncio.sleep(1.0 / FPS)