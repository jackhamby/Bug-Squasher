import pygame, time, math, os
from random import *


screenWidth = 500
screenHeight = 400
gravity = -0.5
level = 1
base_img_url = "/Users/jackhamby/games/bug_squasher/images/"


# Acceleration
# a = (vf - vi) / (tf - ti) 

# Velocity
# v = (xf - xi) / (tf - ti)

def getRandomColor():
    return (randint(0, 255),randint(0, 255),randint(0, 255))

def getRandomXVelocity():
    maxVelocity = math.ceil(level / 2)
    return randint(1, maxVelocity)

def checkScore(score):
    if (score / 1000 in range(0, 10)):
        global level
        level += 1

def tryHatch():
    x = randint(1, 100)
    if (x == 5):
        return True
    else:
        return False


def flush():
    screen.fill((0, 0, 0))




_image_library = {}
def get_image(path):
        global _image_library
        image = _image_library.get(path)
        if image == None:
                image = pygame.image.load(base_img_url + path)
                _image_library[path] = image
        return image



class Bug:
    def __init__(self):
        self.width = 24
        self.height = 17
        self.velocity = [getRandomXVelocity(), 0]
        self.xPos = screenWidth - self.width
        self.yPos = stage.yPos - self.height
        self.color = getRandomColor()
        self.alive = True

    def move(self):
        #print(str(self.velocity[0]))
        self.detect_smash(self.xPos - self.velocity[0])
        self.xPos -= self.velocity[0]
        if (self.xPos < 0):
            self.attack_hero()

    def render(self):
        #print('rendering bug')
        if (self.alive):
            screen.blit(get_image('bug.png'), (self.xPos, self.yPos))

            #pygame.draw.rect(screen, self.color , pygame.Rect(self.xPos, self.yPos, self.width, self.height))
            return True
        else:
            return False

    def attack_hero(self):
        #print('attacking')
        hero.lives -= 1
        self.alive = False

    def detect_smash(self, x_position):

        if(hero.velocity[1] > 0 and ((x_position >= hero.xPos and 
            x_position <= hero.xPos + hero.width) or
            (x_position + self.width >= hero.xPos and 
            x_position + self.width <= hero.xPos + hero.width)) and
            hero.yPos + hero.height >= self.yPos):
                print('hero velocity ' + str(hero.velocity[1]))
                bug.alive = False
                hero.score += 200
                checkScore(hero.score)
        elif (hero.yPos + hero.height == stage.yPos and
            ((x_position >= hero.xPos and 
            x_position <= hero.xPos + hero.width) or
            (x_position + self.width >= hero.xPos and 
            x_position + self.width <= hero.xPos + hero.width))):
                hero.lives -= 2

        # if (x_position <= (hero.xPos + hero.width) and
        #     x_position >= hero.xPos and
        #     self.yPos <= (hero.yPos + hero.width) and
        #     self.yPos >= hero.yPos):
        #     print('detected hero')
        #     bug.alive = False

    


    




class Hero:
    def __init__(self):
        self.width = 22
        self.height = 46
        self.velocity = [3, 1]
        self.xPos = 100
        self.yPos = (2/3) * screenHeight - 100    
        self.color = getRandomColor()
        self.alive = True
        self.score = 0
        self.lives = 10

    def render(self):
        #print('rendering at x:' + str(self.xPos) + ' y:' + str(self.yPos))
        if (self.alive and self.lives > 0):
            #pygame.draw.rect(screen, self.color , pygame.Rect(self.xPos, self.yPos, self.width, self.height))
            screen.blit(get_image('foot_icon.png'), (self.xPos, self.yPos))

            return True

    def jump(self):
        # If not already jumping...
        # print ("stage y pos: " + str(stage.yPos))
        # print("velocity is: " + str(self.velocity[1]))
        if (self.yPos < (stage.yPos - self.height)):
            # print('flying')
            return
        else: 
            self.velocity[1] = -6

    def move(self, x_dir):
        if (self.detect_wall(self.xPos + self.velocity[0])):
            self.xPos -= x_dir * (self.velocity[0])
        # Hit a wall
        else:
            self.velocity[0] = 0

    
    def update(self):
        if (self.detect_ground(self.yPos + self.velocity[1])):
            self.yPos += self.velocity[1]
            self.velocity[1] -= gravity
            #print('updating with new y velcocity')

        # Hit the ground
        else:
            pass
           # self.velocity[1] = 0


    def detect_wall(self, x_position):
        if (x_position >= 0 and (x_position + self.width) <= screenWidth):
            return True

        # Hit wall
        else:
            return False

    def detect_ground(self, y_position):
        if ((y_position + self.height) <= stage.yPos and y_position >= 0 ):
            #print('comparing: ' + str(y_position + self.height) + ' and ' + str(stage.yPos))
            return True

        # Hit ground
        else:
            self.velocity[1] = 0
            return False
        


class Stage:
    def __init__(self):
        self.color = (165,42,42) #Brown
        self.height = (2/3) * screenHeight
        self.width = screenWidth
        self.xPos = 0 
        self.yPos = (2/3) * screenHeight

    def render(self):
        pygame.draw.rect(screen, self.color , pygame.Rect(self.xPos, self.yPos, self.width, self.height))






pygame.init()
screen = pygame.display.set_mode((screenWidth,screenHeight))
done = False

hero = Hero()
stage = Stage()
myfont = pygame.font.SysFont("monospace", 15)
bugs = []




while not done:

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        hero.move(1)
    if keys[pygame.K_d]:
        hero.move(-1)
    if keys[pygame.K_SPACE]:
        hero.jump()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            
    flush()

    hero.update()
    hero.render()
    stage.render()
    if (tryHatch()):
       # print('hatched a bug!!')
        bugs.append(Bug())
    for idx, bug in enumerate(bugs):
        bug.move()
        if (not bug.render()): 
            print('killed bug')
            del bugs[idx]


    scoreLabel = myfont.render("Score: " + str(hero.score), 1, (255,255,0))
    levelLabel = myfont.render("Level: " + str(level), 1, (255,255,0))
    livesLabel = myfont.render("Lives: " + str(hero.lives), 1, (255,255,0))

    screen.blit(scoreLabel, (0, 0))
    screen.blit(levelLabel, (0, 20))
    screen.blit(livesLabel, (0, 40))


    pygame.display.flip()