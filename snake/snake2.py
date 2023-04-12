import pygame, random, sys
from pygame.locals import KEYDOWN, K_UP, K_LEFT, K_RIGHT, K_DOWN, QUIT


def random_cor():
    """
    @return: Retorna uma cor aleatória
    """
    return random.randint(0, 255), random.randint(0, 255),\
           random.randint(0, 255)


def on_grid_random():
    """
    @return: Retorna uma posição aleatória do display
    """
    x = random.randint(0, 590)
    y = random.randint(0, 590)

    return x//10 * 10, y//10 * 10


def colisao(c1, c2):
    """
    @param: Duas tuplas de dois elementos (x, y)
    @return: Retorna True se as tuplas forem iguais.
    """
    return c1[0] == c2[0] and c1[1] == c2[1]


UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption('Snake')

snake = [(200, 200), (210, 200), (220, 200)]
snake_skin = pygame.Surface((10, 10))
snake_skin.fill((0, 255, 0))

fruta_pos = on_grid_random()
fruta = pygame.Surface((10, 10))
fruta.fill((255, 0, 0))

direcao = UP

clock = pygame.time.Clock()
ctrl = 15
while 1:
    clock.tick(ctrl)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == KEYDOWN:
            if event.key == K_UP:
                direcao = UP
            if event.key == K_DOWN:
                direcao = DOWN
            if event.key == K_LEFT:
                direcao = LEFT
            if event.key == K_RIGHT:
                direcao = RIGHT
    
    if colisao(snake[0], fruta_pos):
        fruta_pos = on_grid_random()
        snake.append((0, 0))
        fruta.fill(random_cor())
        ctrl += 0.5
    
    for i in range(len(snake)-1, 0, -1):
        snake[i] = (snake[i-1][0], snake[i-1][1])

    if direcao == UP:
        snake[0] = (snake[0][0], snake[0][1]-10)
    if direcao == DOWN:
        snake[0] = (snake[0][0], snake[0][1]+10)
    if direcao == RIGHT:
        snake[0] = (snake[0][0]+10, snake[0][1])
    if direcao == LEFT:
        snake[0] = (snake[0][0]-10, snake[0][1])

    if snake[0] == (0, 0):
        direcao = RIGHT
    elif snake[0] == (0, 590):
        direcao = UP
    elif snake[0] == (590, 0):
        direcao = DOWN
    elif snake[0] == (590, 590):
        direcao = LEFT
    else:
        if snake[0][0] == 0:
            direcao = UP
        if snake[0][0] == 590:
            direcao = DOWN
        if snake[0][1] == 0:
            direcao = RIGHT
        if snake[0][1] == 590:
            direcao = LEFT

    screen.fill((0, 0, 0))
    screen.blit(fruta, fruta_pos)
    for pos in snake:
        screen.blit(snake_skin, pos)

    pygame.display.update()
