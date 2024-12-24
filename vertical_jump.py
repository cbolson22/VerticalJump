import pygame
import random


##### INITIALIZATION #####

## Start pygame
pygame.init()

## Game Window
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 800

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Vertical Jump')


## Frame Rate
clock = pygame.time.Clock()
FPS = 60


## Game Vars
SCROLL_THRESH = 200
GRAVITY = 1
MAX_BOXES = 10
scroll = 0


## Colors
WHITE = (255, 255, 255)


## Load Images
player_image = pygame.image.load('assets/jump.png').convert_alpha()
background_image = pygame.image.load('assets/background_image.jpg').convert_alpha()
box_image = pygame.image.load('assets/box.png').convert_alpha()



##### CLASSES #####

## Player Class
class Player():
    def __init__(self, x, y) -> None:
        self.image = pygame.transform.scale(player_image, (45, 45))
        self.width = 25
        self.height = 40
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x, y)
        self.vel_y = 0
        self.flip = False


    def move(self):
        ## Reset Vars
        scroll = 0
        dx = 0
        dy = 0

        ## Process Keypresses
        key = pygame.key.get_pressed()
        if key[pygame.K_a] or key[pygame.K_LEFT]:
            dx = -10
            self.flip = True
        elif key[pygame.K_d] or key[pygame.K_RIGHT]:
            dx = 10
            self.flip = False


        ## Gravity
        self.vel_y += GRAVITY
        dy += self.vel_y


        ## Side Conditions
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > WINDOW_WIDTH:
            dx = WINDOW_WIDTH - self.rect.right
        
        ## Collision Checks (y direction)
        for box in box_group:
            if box.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                ## Check if above box
                if self.rect.bottom < box.rect.centery:
                    if self.vel_y > 0:
                        self.rect.bottom = box.rect.top
                        dy = 0
                        self.vel_y = -20

        ## Ground Condition
        if self.rect.bottom + dy > WINDOW_HEIGHT:
            dy = 0
            self.vel_y = -20 


        ## Top of Screen Check
        if self.rect.top <= SCROLL_THRESH:
            ## If player jumping (going up)
            if self.vel_y < 0:
                scroll = -dy


        ## Update rectangle position
        self.rect.x += dx
        self.rect.y += dy + scroll

        return scroll


    def draw(self):
        window.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x - 10 , self.rect.y - 5))
        pygame.draw.rect(window, WHITE, self.rect, 2)


## Box Class
class Box(pygame.sprite.Sprite):
    def __init__(self, x, y, width):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(box_image, (width, 10))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def update(self, scroll):
        ## Update box y pos
        self.rect.y += scroll



## -- Class Instances --
        
## Player Instance
player = Player(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 150)


## Box Instances
box_group = pygame.sprite.Group()

for b in range(MAX_BOXES):
    b_w = random.randint(40,70)
    b_x = random.randint(0, WINDOW_WIDTH - b_w)
    b_y = b * random.randint(80,120)
    box = Box(b_x, b_y, b_w)
    box_group.add(box)



##### GAME #####

## Game Loop
run = True
while run:

    clock.tick(FPS)

    scroll = player.move()

    ## Draw Background
    window.blit(background_image, (0, 0))


    ## Scroll Threshold
    pygame.draw.line(window, WHITE, (0, SCROLL_THRESH), (WINDOW_WIDTH, SCROLL_THRESH))


    ## Update Boxes
    box_group.update(scroll)


    ## Draw Sprites
    box_group.draw(window)
    player.draw()


    ## Event Handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    

    ## Update Display Window
    pygame.display.update()



pygame.quit()