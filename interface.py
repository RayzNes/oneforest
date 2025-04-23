import pygame

def draw_button(screen, font, text, x, y, width, height, active_color, inactive_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, active_color, (x, y, width, height))
        if click[0] == 1 and action:
            action()
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, width, height))

    text_surf = font.render(text, True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=(x + width / 2, y + height / 2))
    screen.blit(text_surf, text_rect)

def draw_interface(screen, font, player, width, height, cyan, brown, white):
    # Панель интерфейса
    pygame.draw.rect(screen, brown, (width - 200, 0, 200, height))

    # Кнопки действий
    draw_button(screen, font, "Вскипятить воду", width - 180, 50, 160, 40, cyan, brown, player.boil_water)
    draw_button(screen, font, "Отдохнуть", width - 180, 100, 160, 40, cyan, brown, player.rest)
    draw_button(screen, font, "Спать", width - 180, 150, 160, 40, cyan, brown, player.sleep)
    draw_button(screen, font, "Собирать", width - 180, 200, 160, 40, cyan, brown, player.forage)
    draw_button(screen, font, "Охотиться", width - 180, 250, 160, 40, cyan, brown, player.hunt)
    draw_button(screen, font, "Поесть", width - 180, 300, 160, 40, cyan, brown, player.eat)
    draw_button(screen, font, "Настой от холода", width - 180, 350, 160, 40, cyan, brown, player.craft_warm_infusion)
    draw_button(screen, font, "Лекарство", width - 180, 400, 160, 40, cyan, brown, player.craft_medicine)
    draw_button(screen, font, "Меховая одежда", width - 180, 450, 160, 40, cyan, brown, player.craft_fur_clothing)

    # Показатели
    y_offset = 500
    screen.blit(font.render(f"Здоровье: {int(player.health)}", True, white), (width - 180, y_offset))
    screen.blit(font.render(f"Жажда: {int(player.thirst)}", True, white), (width - 180, y_offset + 20))
    screen.blit(font.render(f"Голод: {int(player.hunger)}", True, white), (width - 180, y_offset + 40))
    screen.blit(font.render(f"Тепло: {int(player.warmth)}", True, white), (width - 180, y_offset + 60))
    screen.blit(font.render(f"Травничество: {player.herbalism}", True, white), (width - 180, y_offset + 80))
    screen.blit(font.render(f"Собирательство: {player.foraging}", True, white), (width - 180, y_offset + 100))
    screen.blit(font.render(f"День: {player.day} ({player.season})", True, white), (10, 10))
    screen.blit(font.render(f"Болезнь: {'Да' if player.is_sick else 'Нет'}", True, white), (width - 180, y_offset + 120))
    screen.blit(font.render(f"Дни без сна: {player.days_without_sleep}", True, white), (width - 180, y_offset + 140))

    # Инвентарь
    screen.blit(font.render("Инвентарь:", True, white), (width - 180, y_offset + 160))
    for i, (item, count) in enumerate(player.inventory.items()):
        screen.blit(font.render(f"{item}: {count}", True, white), (width - 180, y_offset + 180 + i * 20))