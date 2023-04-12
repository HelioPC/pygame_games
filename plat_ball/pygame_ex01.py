from os import path
import pygame
from pygame.locals import *
from random import choice
from time import sleep

# pip install pygame --pre --user
# Dimensões
LARG = 700
ALT = 500
MEIOLARG = LARG//2
MEIOALT = ALT//2
# Cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
PP = (255, 0, 255)
YEL = (255, 255, 0)
# Direções
UP = 2
DOWN = 4
DOWNLEFT = 1
DOWNRIGHT = 3
UPLEFT = 7
UPRIGHT = 9
# Velocidade
VEL = 10

ABS_PATH = path.abspath('.')

pygame.init()
screen = pygame.display.set_mode((LARG, ALT), 0)
d = pygame.image.load(ABS_PATH + '/carvalho.png').convert_alpha()
d = pygame.transform.scale(d, (32, 32))
pygame.display.set_icon(d)
pygame.display.set_caption('P Y G A M E  E X 0 1')


class Bola:
    def __init__(self, tela, cor, centro, raio):
        self.centro = centro
        self.raio = raio
        self.tela = tela
        self.cor = cor
        self.dir = choice([UPLEFT, UPRIGHT, DOWNLEFT, DOWNRIGHT])

    def desenha(self):
        pygame.draw.circle(self.tela, self.cor, self.centro, self.raio, 0)

    def move(self, pos1=LARG-10, pos2=10):
        if self.dir == UPLEFT:
            self.centro[0] -= VEL
            self.centro[1] -= VEL
        if self.dir == UPRIGHT:
            self.centro[0] += VEL
            self.centro[1] -= VEL
        if self.dir == DOWNLEFT:
            self.centro[0] -= VEL
            self.centro[1] += VEL
        if self.dir == DOWNRIGHT:
            self.centro[0] += VEL
            self.centro[1] += VEL

        if self.centro[0] <= pos2:
            if self.dir == UPLEFT:
                self.dir = UPRIGHT
            if self.dir == DOWNLEFT:
                self.dir = DOWNRIGHT
        if self.centro[1] <= pos2:
            if self.dir == UPLEFT:
                self.dir = DOWNLEFT
            if self.dir == UPRIGHT:
                self.dir = DOWNRIGHT
        if self.centro[0] >= pos1:
            if self.dir == UPRIGHT:
                self.dir = UPLEFT
            if self.dir == DOWNRIGHT:
                self.dir = DOWNLEFT

    def colisao(self):
        return self.centro[0] == LARG-10 or self.centro[1] == 10 or\
               self.centro[0] == 10


class Bloco:
    def __init__(self, left, top, larg, alt, direcao=UP):
        self.left = left
        self.top = top
        self.larg = larg
        self.alt = alt
        self.dir = direcao

    def set_bloco(self):
        return pygame.Rect(self.left, self.top, self.larg, self.alt)

    def move(self):
        if self.dir == UP:
            self.top -= 10
        if self.dir == DOWN:
            self.top += 10

        if self.top == ALT-120:
            self.dir = UP
        if self.top == 10:
            self.dir = DOWN


font = pygame.font.SysFont(None, 40)
pal = font.render('0', True, WHITE)
pal_r = pal.get_rect()
pal_r.centerx = screen.get_rect().centerx
pal_r.centery = screen.get_rect().centery - 200
ctrl = 0

bell = pygame.mixer.Sound(ABS_PATH + '/impact_medium1.wav')
coll = pygame.mixer.Sound(ABS_PATH + '/bell03.wav')

plat = pygame.Rect(MEIOLARG, ALT-10, 70, 10)
bola = Bola(screen, RED, [MEIOLARG, MEIOALT], 6)


def gameover(b: Bola) -> bool:
    return b.centro[1] > ALT


clock = pygame.time.Clock()
while 1:
    clock.tick(20)
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_LEFT and plat.left >= 50:
                plat.left -= 50
            if event.key == K_RIGHT and plat.right <= LARG - 50:
                plat.left += 50

        if event.type == QUIT:
            pal = font.render('GAME OVER', True, RED)
            pal_r.centerx -= 72
            pal_r.centery += 70
            screen.blit(pal, pal_r)
            pygame.display.update()
            sleep(1.5)
            pygame.quit()
            exit()

    screen.fill((0, 0, 0))

    pygame.draw.rect(screen, BLUE, plat)
    '''pygame.draw.rect(screen, YEL, b1.set_bloco())
    pygame.draw.rect(screen, PP, b2.set_bloco())
    b1.move()
    b2.move()'''
    bola.desenha()
    bola.move()

    for i in range(-10, 81, 10):
        if bola.centro[1] == ALT-20 and bola.centro[0] == plat.left+i:
            coll.play()
            if bola.dir == DOWNLEFT:
                bola.dir = UPLEFT
                ctrl += 1
            if bola.dir == DOWNRIGHT:
                bola.dir = UPRIGHT
                ctrl += 1

    pal = font.render(str(ctrl), True, WHITE)
    screen.blit(pal, pal_r)

    if bola.colisao():
        bell.play()

    if gameover(bola):
        pal = font.render('GAME OVER', True, RED)
        pal_r.centerx -= 72
        pal_r.centery += 70
        screen.blit(pal, pal_r)
        pygame.display.update()
        sleep(1.5)
        pygame.quit()
        exit()

    pygame.display.update()
