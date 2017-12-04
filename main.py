#!usr/bin/env python
# Comet Crush
# music by AphixSky
# Art by Kenny
import pygame
import random
from os import path
import os


# finds the directory to img
img_dir = path.join(path.dirname(__file__),'img')
# find the directory to sound
sound_dir = path.join(path.dirname(__file__),'sound')


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
screen = pygame.display.set_mode((WIDTH, HEIGHT)) # sets the creen
pygame.display.set_caption("Shooter")
clock = pygame.time.Clock()
STATE = 0 # state the game is currently at 0 = menu, 1 = playing, 2 = end Screen
musicplaying = False # variable to check if the music is playing


# display any text to screen
def displayMsg(msg,font,size,color,x,y):
    myfont = pygame.font.SysFont(font,size,True) # gets font/font size/ bold
    label = myfont.render(msg,1,color); # makes a label with a msg and color with it
    screen.blit(label,(x,y)) # stages label to screen at x and y cordinate

# opens the highscore file then reads and returns the highscore
def getHighScore():
    highscore_file = open("high_score.txt","r")
    high_score = int(highscore_file.read())
    highscore_file.close()
    return high_score

# writes new highscore to the highscore file
def writeHighScore(highscore):
    highscore_file = open("high_score.txt","w")
    highscore_file.write(str(highscore))
    highscore_file.close()


# explosion sprite class
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = explosion_img[0]# starting explosion_img
        self.rect = self.image.get_rect()
        self.rect.center = center # center of explosion
        self.frame = 0 # starting animation frame
        self.last_update = pygame.time.get_ticks() # last update of animation
        self.frame_rate = 25 # frame rate of explosion time

    def update(self):
        now = pygame.time.get_ticks()
        # if its time for next frame
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            # kill sprite at end of animation
            if self.frame == len(explosion_img):
                self.kill()
            else:
                center = self.rect.center # set to current center
                self.image = explosion_img[self.frame] # advance frame
                self.rect = self.image.get_rect()
                self.rect.center = center

# player ship class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        # sets the player image to specefic size // load image
        self.image = pygame.transform.scale(player_img, (50,38))
        self.image.set_colorkey(BLACK) # gets rid of Black outline
        self.rect = self.image.get_rect()

        # hit circle of the player ship
        self.radius = 20
        self.rect.centerx = WIDTH/2 # x cordinate of sprite
        self.rect.bottom = HEIGHT - 10 # y cordinate of sprite
        self.speedx = 0 # player does not move til gets command

        self.shoot_delay = 180 # shot delay inbetween shots
        self.last_shot = pygame.time.get_ticks()
    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed() # every key that is pushed down

        # deals with key movement
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        if keystate[pygame.K_SPACE]:
            self.shoot()

        # moves the player along the x cordinate
        self.rect.x += self.speedx

        #create walls for player
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            #creates shot sprite starting point is top of player sprite
            shot = Shot(self.rect.centerx, self.rect.top)
            all_sprites.add(shot) # add shot sprite to all sprites
            shots.add(shot) # add shot to shots gropup
            laser_sound.play()


# enemy units
class Mob(pygame.sprite.Sprite):
    def __init__(self,baseSpeed,topSpeed):
        pygame.sprite.Sprite.__init__(self)

        # load image of asteroid
        self.image_og = random.choice(asteroid_img)
        self.image_og.set_colorkey(BLACK)

        # copy image into another image
        self.image = self.image_og.copy()
        self.rect = self.image.get_rect()

        # hit circle of asteroid
        self.radius = int(self.rect.width * 0.9 / 2)

        # enemy appears off screen in random location
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150,-100)

        # enemy gets random x and y speed it travels
        # self.speedy = random.randrange(3,15)
        self.baseSpeed = baseSpeed
        self.topSpeed = topSpeed
        self.speedy = random.randrange(self.baseSpeed,self.topSpeed)
        print(self.speedy)
        self.speedx = random.randrange(-3,3)

        self.rot = 0 # rotation
        self.rot_speed = random.randrange(-9,9) # random rotation speed
        self.last_update = pygame.time.get_ticks() # last update

    # rotates the image
    def rotate(self):
        now = pygame.time.get_ticks()
        # miliseconds since last roation
        if now - self.last_update > 50:
            self.last_update = now
            # rotation speed
            self.rot = (self.rot + self.rot_speed) % 360

            # saves the rotated image in a new image
            image_new = pygame.transform.rotate(self.image_og,self.rot)
            center_old = self.rect.center # get the old mob center

            # saves the image
            self.image = image_new
            self.rect = self.image.get_rect() # draws a new rectangle around it
            self.rect.center = center_old #keeps it centered at same spot
    #updates/moves the image
    def update(self):
        self.rotate()
        # moves the unit at a set speed x and y
        self.rect.y += self.speedy
        self.rect.x += self.speedx

        #if the mob goes off the screen reset the mob to a random location again
        if self.rect.top > HEIGHT + 10 or self.rect.left < -20 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100,-30)
            self.speedy = random.randrange(self.baseSpeed,self.topSpeed)



# shots fire
class Shot(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)

        # load the image
        self.image = laser_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

        # sets the bottom and center to given x and y
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -15

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill() #deletes sprite


#load all game graphics
background = pygame.image.load(path.join(img_dir,"space3.jpg")).convert()
background_rect = background.get_rect()

# load in a random ship
ship_list = ["shipRed.png","shipBlue.png","shipOrange.png","shipGreen.png"]
player_img = pygame.image.load(path.join(img_dir,ship_list[random.randint(0,3)])).convert()
laser_img = pygame.image.load(path.join(img_dir,"laser.png")).convert()



asteroid_img = []
asteroid_list = ['asteroid.png','asteroid1.png','asteroid2.png','asteroid3.png','asteroid4.png'
                ,'asteroid5.png','asteroid6.png','asteroid7.png',]
for img in asteroid_list:
    asteroid_img.append(pygame.image.load(path.join(img_dir,img)).convert())

explosion_img = []
explosion_list = ['explosion.png','explosion2.png','explosion3.png'
                ,'explosion4.png','explosion5.png','explosion6.png','explosion7.png','explosion8.png']
for img in explosion_list:
    expl = pygame.image.load(path.join(img_dir,img)).convert()
    expl.set_colorkey(BLACK)
    explosion_img.append(pygame.transform.scale(expl,(75,75)))

# load game sound
laser_sound = pygame.mixer.Sound(path.join(sound_dir,"Laser.wav"))
laser_sound.set_volume(0.20)
pygame.mixer.music.load(path.join(sound_dir,'background.wav'))
pygame.mixer.music.set_volume(0.3)

explosion_snd = []

explosion_list = ['explosion.wav','explosion2.wav','explosion3.wav','explosion4.wav']
for snd in explosion_list:
    explosion_snd.append(pygame.mixer.Sound(path.join(sound_dir,snd)))
for snd in explosion_snd:
    snd.set_volume(0.25)

die_snd = pygame.mixer.Sound(path.join(sound_dir,"die.wav"))
die_snd.set_volume(0.20)

difficultySettings = ['EASY','NORMAL','HARD','INSANE']

difficulty = difficultySettings[1]
difficultyIndex = 1
# Sprite Groups
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
shots = pygame.sprite.Group()






# Start menu
#First game state the Menu: 0
def menu():
    global player_img, player, STATE, musicplaying, difficulty, difficultyIndex

    colorIndex = 0

    start = False
    while start != True:
        screen.blit(background,background_rect)
        displayMsg("Asteroid Assault","monospace",38,WHITE,20,100)
        displayMsg("Current High Score:" + str(high_score),"monospace",25,WHITE,43,HEIGHT/2 - 24)
        displayMsg("Press SPACE to Play!","monospace",25,WHITE,60,HEIGHT/2)
        displayMsg("Press C to Change Ship","monospace",25,WHITE,40,HEIGHT/2+25)
        displayMsg("Press M to Toggle Music","monospace",25,WHITE,40,HEIGHT/2+45)
        displayMsg("  Press H for Manual","monospace",25,WHITE,40,HEIGHT/2+65)
        displayMsg("Difficulty: ","monospace",28,WHITE,43,HEIGHT - 28)
        if(difficulty == "EASY"):
            displayMsg(str(difficulty),"monospace",28,GREEN,240,HEIGHT - 28)
        elif(difficulty == "NORMAL"):
            displayMsg(str(difficulty),"monospace",28,WHITE,240,HEIGHT - 28)
        elif(difficulty == "HARD"):
            displayMsg(str(difficulty),"monospace",28,YELLOW,240,HEIGHT - 28)
        elif(difficulty == "INSANE"):
            displayMsg(str(difficulty),"monospace",28,RED,240,HEIGHT - 28)






        player_img = pygame.transform.scale(player_img, (70,58))
        player_img.set_colorkey(BLACK)
        screen.blit(player_img,(WIDTH/2-20,HEIGHT/2-120))
        # *after* drawing everything, flip the display
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start = True
                    # # create and add player to sprite group
                    player = Player()
                    all_sprites.add(player)
                    # loop the background music
                    # pygame.mixer.music.play(loops= -1)
                    STATE = 1
                if event.key == pygame.K_c:
                    if(colorIndex == 4):
                        colorIndex = 0
                    player_img = pygame.image.load(path.join(img_dir,ship_list[colorIndex])).convert()
                    colorIndex += 1
                if event.key == pygame.K_h:
                    os.system('open -e manual.txt')
                if event.key == pygame.K_d:

                    difficultyIndex += 1
                    if(difficultyIndex == 4):
                        difficultyIndex = 0

                    difficulty = difficultySettings[difficultyIndex]

                    print(difficulty)
                if event.key == pygame.K_m:
                    if(musicplaying == False):
                        pygame.mixer.music.set_volume(0.3)
                        pygame.mixer.music.play(loops = -1)
                        musicplaying = True
                    else:
                        pygame.mixer.music.set_volume(0)
                        musicplaying = False



# the main game state: 1
def main():
    global player, all_sprites,difficulty

    # check the difficulty
    if (difficulty == "EASY"):
        mobcount = 7
        scoreModifier = 0.7
        baseSpeed = 1
        topSpeed = 12
        print("EASY difficulty")
    elif(difficulty == "NORMAL"):
        mobcount = 10
        scoreModifier = 1
        baseSpeed = 3
        topSpeed = 15
        print("NORMAL difficulty")
    elif(difficulty == "HARD"):
        mobcount = 13
        scoreModifier = 1.5
        baseSpeed = 5
        topSpeed = 17
        print("HARD difficulty")
    elif(difficulty == "INSANE"):
        mobcount = 15
        scoreModifier = 3
        baseSpeed = 7
        topSpeed = 17
        print("INSANE difficulty")

    # spawn range between 0-10
    for i in range(mobcount):
        m = Mob(baseSpeed,topSpeed)
        # add mob to groups
        all_sprites.add(m)
        mobs.add(m)

    score = 0
    hitscore = 0
    # Game loop
    running = True
    pause = False
    while running:
        # keep loop running at the right speed
        clock.tick(FPS)

        # Process input (events)
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                # if player wants to pause
                if event.key == pygame.K_p:
                    if(pause):
                        pause = False
                    else:
                        pause = True
                # exit the game from pause state
                if event.key == pygame.K_RETURN:
                    if(pause):
                        score = -2 # indicate to state machine we want to end
                        return score

                # exit to main menu
                if event.key == pygame.K_ESCAPE:
                    if(pause):
                        # delete the sprites
                        all_sprites.empty()
                        mobs.empty()
                        shots.empty()
                        score = -1
                        return score



        # Update
        if(pause != True):
            all_sprites.update()

        #check to see if a bullet hit a mob if hit bullet and mob get deleted
        hits = pygame.sprite.groupcollide(mobs,shots, True, True)


        # if a hit lands spawn more mobs
        for hit in hits:
            m = Mob(baseSpeed,topSpeed)
            all_sprites.add(m)
            mobs.add(m)
            score += int((50 - hit.radius)/2 * scoreModifier)
            hitscore += 1
            explosion = Explosion(hit.rect.center)
            all_sprites.add(explosion)
            random.choice(explosion_snd).play()

        #check to see if a mob hit player (returns list of mobs that hit players)
        # make collision circler
        hits = pygame.sprite.spritecollide(player, mobs, False,pygame.sprite.collide_circle)

        # player is hit
        if hits:
            # spawns player explosion
            die_explosion = Explosion(player.rect.center)
            all_sprites.add(die_explosion)
            player.kill()
            # play die sound and end game loop
            die_snd.play()

        if not player.alive() and not die_explosion.alive():
            all_sprites.empty()
            mobs.empty()
            shots.empty()
            running = False
            return score

        # Draw / render
        screen.fill(BLACK)
        screen.blit(background,background_rect)

        #label = myfont.render("Score:" + str(score),1, WHITE)
        #screen.blit(label,(100,0))

        displayMsg("Score:" + str(score),"monospace",20,WHITE,0,0) # display score board
        if score > high_score:
            displayMsg("HighScore:" + str(score),"monospace",20,WHITE,220,0) # display high score
        else:
            displayMsg("HighScore:" + str(high_score),"monospace",20,WHITE,220,0) # display high score



        all_sprites.draw(screen)

        # when the game is in the pause state show pause options
        if(pause):
            displayMsg("PAUSED","monospace",50,WHITE,110,HEIGHT/2-10)
            displayMsg("PRESS RETURN TO EXIT GAME","monospace",22,WHITE,32,HEIGHT/2+50)
            displayMsg("PRESS ESC TO RETURN TO MENU","monospace",22,WHITE,25,HEIGHT/2+70)


        # *after* drawing everything, flip the display
        pygame.display.flip()




# the end screen state of the game : 2
def endScreen():
    global STATE, run,higher,high_score, all_sprites,player
    quit = False
    while quit != True:

        screen.fill(BLACK)
        screen.blit(background,background_rect)
        # if the player got a high score, displays and writes new high score
        if higher:
            displayMsg("New High Score!!!","monospace",25,WHITE,80,30)
            displayMsg("Score:" + str(score),"monospace",25,WHITE,140,HEIGHT/2)
            displayMsg("Press SPACE to Try Again!","monospace",25,WHITE,25,HEIGHT/2+20)
            displayMsg("Press ESC for MainMenu","monospace",25,WHITE,40,HEIGHT/2+40)
            displayMsg("Press ENTER to quit","monospace",25,WHITE,50,HEIGHT/2+60)
            writeHighScore(score)
            high_score = score
            pygame.display.flip()

        # regular score
        else:
            displayMsg("Score:" + str(score),"monospace",25,WHITE,140,HEIGHT/2)
            displayMsg("Press SPACE to Try Again!","monospace",25,WHITE,25,HEIGHT/2+20)
            displayMsg("Press ESC for MainMenu","monospace",25,WHITE,40,HEIGHT/2+40)
            displayMsg("Press ENTER to quit","monospace",25,WHITE,50,HEIGHT/2+60)


            pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    quit = True
                    run = False
                if event.key == pygame.K_SPACE:
                    player = Player()
                    all_sprites.add(player)
                    STATE = 1
                    quit = True
                if event.key == pygame.K_ESCAPE:
                    STATE = 0
                    quit = True



high_score = getHighScore() # get the high score
run = True

while(run):

    # menu state
    if(STATE == 0):
        menu()
    # main game state
    elif(STATE == 1):
        score = main()

        #signal to back to main menu
        if(score == -1):
            STATE = 0
        # signal to quit from pause
        elif(score == -2):
            run = False
        else:
            # if score > highscore
            higher = False
            if score > high_score:
                higher = True
            STATE = 2
    # end game state
    elif(STATE == 2):
        endScreen()

pygame.quit()
