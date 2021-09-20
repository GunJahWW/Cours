import pygame
from fruit import Fruit
from random import randint

pygame.mixer.pre_init(44100, -16, 1, 512) # важно прописать до pygame.init()
pygame.init()
pygame.time.set_timer(pygame.USEREVENT, 2000)

pygame.mixer.music.load('sounds/bird.mp3')
pygame.mixer.music.play(-1)

s_catch = pygame.mixer.Sound('sounds/catch.ogg')

BLACK = (0, 0, 0)
W, H = 600, 500

sc = pygame.display.set_mode((W, H))

clock = pygame.time.Clock()
FPS = 60

score = pygame.image.load('images/score_fon.png').convert_alpha()
f = pygame.font.SysFont('arial', 30)

korzina = pygame.image.load('images/korzina2.png').convert_alpha()
t_rect = korzina.get_rect(centerx=W//2, bottom=H-5)

fruits_data = ({'path': 'apple.png', 'score': 100},
              {'path': 'pear.png', 'score': 150},
              {'path': 'prune.png', 'score': 200})

fruits_surf = [pygame.image.load('images/'+data['path']).convert_alpha() for data in fruits_data]

def createFruits(group):
    indx = randint(0, len(fruits_surf)-1)
    x = randint(20, W-20)
    speed = randint(1, 4)

    return Fruit(x, speed, fruits_surf[indx], fruits_data[indx]['score'], group)

game_score = 0
game_life = 0


def collideFruits():
    global game_score, game_life
    for fruit in fruits:
        if t_rect.collidepoint(fruit.rect.center):
            s_catch.play()
            game_score += fruit.score
            fruit.kill()
        elif fruit.rect.bottom >= H+5:
            game_life -= 1
            fruit.kill()

fruits = pygame.sprite.Group()

bg = pygame.image.load('images/back3.png').convert()

speed = 10
createFruits(fruits)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or game_life == -3:
            exit()
        elif event.type == pygame.USEREVENT:
            createFruits(fruits)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        t_rect.x -= speed
        if t_rect.x < 0:
            t_rect.x = 0
    elif keys[pygame.K_RIGHT]:
        t_rect.x += speed
        if t_rect.x > W-t_rect.width:
            t_rect.x = W-t_rect.width

    collideFruits()

    sc.blit(bg, (0, 0))
    sc.blit(score, (0, 0))
    sc_text = f.render(str(game_score), 1, (94, 138, 14))
    sc.blit(sc_text, (20, 10))

    fruits.draw(sc)
    sc.blit(korzina, t_rect)
    pygame.display.update()

    clock.tick(FPS)

    fruits.update(H)

