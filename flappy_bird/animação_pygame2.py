"""
Recriação do jogo flappy bird
"""

from random import randint
from time import sleep
import sys
import pygame
from pygame.locals import KEYDOWN, K_w, QUIT, K_SPACE

# Norton V = Yfcoxy20Wulpufbi2000
# DSC = 0t1pr4hiDrathlflmaz6

LARG = 450
ALT = 650
VEL = 15
G = 2
JOGO_VEL = 10
GROUND_ALT = 100
GROUND_LARG = LARG * 2
CANO_LARG = 80
CANO_ALT = 500
CANO_SP = 200


class Bird(pygame.sprite.Sprite):
    """
    Classe que representa o pássaro
    """

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.images = [pygame.image.load('./bluebird-upflap.png').convert_alpha(),
                       pygame.image.load('./bluebird-midflap.png').convert_alpha(),
                       pygame.image.load('./bluebird-downflap.png').convert_alpha()]

        self.image = pygame.image.load('./bluebird-upflap.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)

        self.speed = VEL

        self.current_image = 0

        self.rect = self.image.get_rect()
        self.rect[0] = LARG//2
        self.rect[1] = ALT//2

    def update(self):
        """
        Função que atualiza a imagem do pássaro
        """
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image]

        self.speed += G

        self.rect[1] += self.speed

    def sobe(self):
        """
        Uma vez chamada, faz o pássaro dar um salto
        """
        self.speed = -VEL


class Ground(pygame.sprite.Sprite):
    """
    Classe que representa o chão
    """
    def __init__(self, xpos):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('./base.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (GROUND_LARG,
                                                         GROUND_ALT))
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = ALT - GROUND_ALT

    def update(self):
        """
        Atualiza o chão
        """
        self.rect[0] -= JOGO_VEL


class Cano(pygame.sprite.Sprite):
    """
    Classe que representa os canos
    """
    def __init__(self, inverted, xpos, ysize):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('./pipe-red.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (CANO_LARG, CANO_ALT))

        self.rect = self.image.get_rect()
        self.rect[0] = xpos

        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[1] = - (self.rect[3] - ysize)
        else:
            self.rect[1] = ALT - ysize

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        """
        Atualiza a posição em que se encontra o cano
        """
        self.rect[0] -= JOGO_VEL


def is_off_screen(sprite):
    """
    Verifica se o sprite está fora do ecrã
    """
    return sprite.rect[0] < -(sprite.rect[2])


def get_random_cano(xpos):
    """
    Retorna 2 canos em uma posição aleatória
    """
    size = randint(100, 300)
    cano = Cano(False, xpos, size)
    cano_inv = Cano(True, xpos, ALT - size - CANO_SP)

    return cano, cano_inv


pygame.init()
screen = pygame.display.set_mode((LARG, ALT), 0, 32)
pygame.display.set_caption('F L A P P Y  B I R D !')
BACKGROUND = pygame.image.load('./background-day2.png')
BACKGROUND = pygame.transform.scale(BACKGROUND, (LARG, ALT))

bird_group = pygame.sprite.Group()
bird = Bird()
bird_group.add(bird)

ground_group = pygame.sprite.Group()

cano_group = pygame.sprite.Group()

def jogo():
    """
    Função que inicia o jogo
    """
    for i in range(2):
        ground = Ground(GROUND_LARG * i)
        ground_group.add(ground)

    for i in range(2):
        canos = get_random_cano(LARG * i + 800)
        cano_group.add(canos[0])
        cano_group.add(canos[1])

    font = pygame.font.SysFont(None, 40)

    pont = font.render('0', True, (255, 255, 255))
    pont_r = pont.get_rect()
    pont_r.centerx = screen.get_rect().centerx
    pont_r.centery = screen.get_rect().centery - 250
    ctrl = 0

    clock = pygame.time.Clock()
    j = 25
    while 1:
        clock.tick(j)
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_SPACE or event.key == K_w:
                    bird.sobe()

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(BACKGROUND, (0, 0))

        if is_off_screen(ground_group.sprites()[0]):
            ground_group.remove(ground_group.sprites()[0])

            new_ground = Ground(GROUND_LARG - 20)
            ground_group.add(new_ground)

        if is_off_screen(cano_group.sprites()[0]):
            cano_group.remove(cano_group.sprites()[0])
            cano_group.remove(cano_group.sprites()[0])

            canos = get_random_cano(LARG * 2)

            cano_group.add(canos[0])
            cano_group.add(canos[1])

        bird_group.update()
        ground_group.update()
        cano_group.update()

        bird_group.draw(screen)
        cano_group.draw(screen)
        ground_group.draw(screen)

        screen.blit(pont, pont_r)

        if cano_group.sprites()[0].rect[0] == 200:
            ctrl += 1
            j += 0.5

        pont = font.render(str(ctrl), True, (255, 255, 255))

        pygame.display.update()

        if pygame.sprite.groupcollide(bird_group, ground_group, False, False,
        pygame.sprite.collide_mask) or pygame.sprite.groupcollide(bird_group,
        cano_group, False, False, pygame.sprite.collide_mask):
            sleep(1.3)
            pygame.quit()
            sys.exit()

def jogo_parado():
    """
    @param: None
    @return: None
    """

if __name__ == '__main__':
    jogo()
