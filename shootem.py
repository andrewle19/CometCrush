import pygame
import random
from os import path

# finds the directory to img
img_dir = path.join(path.dirname(__file__),'img')

WIDTH = 400
HEIGHT = 600
FPS = 60

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


# initialize pygame and create window
pygame.init()
pygame.mixer.init() # deals with sound
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooter")
clock = pygame.time.Clock()

# player ship class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # sets the player image to specefic size
        self.image = pygame.transform.scale(player_img, (50,38))
        # gets rid of Black outline
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.centerx = WIDTH/2 # x cordinate of sprite
        self.rect.bottom = HEIGHT - 10 # y cordinate of sprite
        self.speedx = 0

    def update(self):

        self.speedx = 0
        keystate = pygame.key.get_pressed() # every key that is pushed down
        # deals with key movement
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        self.rect.x += self.speedx
        #create walls for player
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        # starting point is top of player sprite
        shot = Shot(self.rect.centerx, self.rect.top)
        all_sprites.add(shot) # add shot sprite to all sprites
        shots.add(shot) # add shot to shots gropup


# enemy units
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = asteroid_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        # hit circle of asteroid
        self.radius = int(self.rect.width * 0.9 / 2)
        # enemy appears off screen in random location
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100,-40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3,3)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 10 or self.rect.left < -20 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100,-30)
            self.speedy = random.randrange(1, 9)



# shots fire
class Shot(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = laser_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -15

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill() #deletes sprite


#load all game graphics
background = pygame.image.load(path.join(img_dir,"space.jpg")).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir,"ship.png")).convert()
asteroid_img = pygame.image.load(path.join(img_dir,"asteroid.png")).convert()
laser_img = pygame.image.load(path.join(img_dir,"laser.png")).convert()



all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
shots = pygame.sprite.Group()
player = Player()
all_sprites.add(player) # add player sprite to pygame

# spawn range between 0-8
for i in range(10):
    m = Mob()
    # add mob to groups
    all_sprites.add(m)
    mobs.add(m)
score = 0
myfont = pygame.font.SysFont("monospace",15)


# Game loop
running = True
while running:

    # keep loop running at the right speed
    clock.tick(FPS)

    # Process input (events)
    for event in pygame.event.get():

        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        # key was pressed down
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()



    # Update
    all_sprites.update()

    #check to see if a bullet hit a mob if hit bullet and mob get deleted
    hits = pygame.sprite.groupcollide(mobs,shots, True, True)


    # if a hit lands spawn more mobs
    for hit in hits:
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)
        score += 1

    #check to see if a mob hit player (returns list of mobs that hit players)
    # make collision circler
    hits = pygame.sprite.spritecollide(player, mobs, False,pygame.sprite.collide_circle)

    # game loop will end
    if hits:
        running = False

    # Draw / render
    screen.fill(BLACK)
    screen.blit(background,background_rect)
    label = myfont.render("Score:" + str(score),1, WHITE)
    screen.blit(label,(0,0))
    all_sprites.draw(screen)

    # *after* drawing everything, flip the display
    pygame.display.flip()
pygame.quit()
