import asyncio
import platform
import pygame
import random

# Инициализация Pygame
pygame.init()

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

# Глобальные переменные
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Один в лесу 2")
clock = pygame.time.Clock()
font = pygame.font.Font(None, FONT_SIZE)

# Параметры игрока
health = 100
thirst = 100
warmth = 100
herbalism = 0
foraging = 0
medicine = 0
season = "winter"  # Начнем с зимы
day = 1

# Функции кнопок
def draw_button(text, x, y, width, height, active_color, inactive_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, active_color, (x, y, width, height))
        if click[0] == 1 and action:
            action()
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, width, height))

    text_surf = font.render(text, True, WHITE)
    text_rect = text_surf.get_rect(center=(x + width / 2, y + height / 2))
    screen.blit(text_surf, text_rect)

def boil_water():
    global thirst
    thirst = min(100, thirst + 20)

def rest():
    global health
    health = min(100, health + 10)

def forage():
    global foraging, herbalism
    foraging += 5
    herbalism += random.randint(0, 3)

# Основные функции игры
def setup():
    pass  # Инициализация уже выполнена выше

def update_loop():
    global health, thirst, warmth, day, season

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return

    # Эффекты сезона
    if season == "winter":
        warmth -= 0.5
    elif season == "summer":
        warmth += 0.5
        thirst -= 0.3

    # Обновление состояния
    thirst -= 0.2
    health -= 0.1 if warmth < 30 or thirst < 30 else 0
    warmth = max(0, min(100, warmth))
    thirst = max(0, min(100, thirst))
    health = max(0, min(100, health))

    # Смена дня и сезона
    if pygame.time.get_ticks() % 10000 < 100:  # Каждые 10 секунд новый день
        day += 1
        if day % 10 == 0:
            season = "summer" if season == "winter" else "winter"

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
    warmth += 0.1 if 150 <= 100 <= 170 and 320 <= 300 <= 340 else 0

    # Интерфейс
    pygame.draw.rect(screen, BROWN, (WIDTH - 200, 0, 200, HEIGHT))
    draw_button("Boil water", WIDTH - 180, 50, 160, 40, CYAN, BROWN, boil_water)
    draw_button("Rest", WIDTH - 180, 100, 160, 40, CYAN, BROWN, rest)
    draw_button("Forage", WIDTH - 180, 150, 160, 40, CYAN, BROWN, forage)

    # Показатели
    screen.blit(font.render(f"Health: {int(health)}", True, WHITE), (WIDTH - 180, 200))
    screen.blit(font.render(f"Thirst: {int(thirst)}", True, WHITE), (WIDTH - 180, 220))
    screen.blit(font.render(f"Warmth: {int(warmth)}", True, WHITE), (WIDTH - 180, 240))
    screen.blit(font.render(f"Herbalism: {herbalism}", True, WHITE), (WIDTH - 180, 260))
    screen.blit(font.render(f"Foraging: {foraging}", True, WHITE), (WIDTH - 180, 280))
    screen.blit(font.render(f"Day: {day} ({season})", True, WHITE), (10, 10))

    pygame.display.flip()

async def main():
    setup()
    while health > 0:
        update_loop()
        await asyncio.sleep(1.0 / FPS)

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())