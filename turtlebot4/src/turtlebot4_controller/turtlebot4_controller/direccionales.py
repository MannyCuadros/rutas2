import pygame
import sys

def print_key_state(window, font, x, a):
    window.fill((0, 0, 0))
    text_x = font.render("x = {}".format(x), True, (255, 255, 255))
    text_a = font.render("a = {}".format(a), True, (255, 255, 255))
    window.blit(text_x, (20, 20))
    window.blit(text_a, (20, 60))
    pygame.display.flip()

def main():
    # Inicializar pygame
    pygame.init()

    # Definir el tamaño de la ventana
    window_width = 200
    window_height = 100
    window = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Control")

    # Definir fuente
    font = pygame.font.Font(None, 36)

    # Definir las variables para el estado de las teclas
    x = 0
    a = 0

    # Bucle principal
    while True:
        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    x = 1
                elif event.key == pygame.K_DOWN:
                    x = -1
                elif event.key == pygame.K_RIGHT:
                    a = 1
                elif event.key == pygame.K_LEFT:
                    a = -1
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    x = 0
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    a = 0
        
        # Imprimir el estado de las teclas en la ventana de Pygame
        print_key_state(window, font, x, a)

if __name__ == "__main__":
    main()