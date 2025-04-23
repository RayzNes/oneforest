import asyncio
import platform
import pygame
from game import setup, update_loop, main

# Инициализация Pygame
pygame.init()

# Вызов setup для инициализации ресурсов игры
setup()

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())