import pygame
import random
import os


##### INITIALIZATION #####

## Start pygame
pygame.init()

## Game Window
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600

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
bg_scroll = 0
game_over = False
score = 0
fade_counter = 0

if os.path.exists('score.txt'):
    with open('score.txt', 'r') as file:
        high_score = int(file.read())
else:
    high_score = 0


## Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PANEL = (153, 217, 234)


## Fonts
font_small = pygame.font.SysFont('Lucida Sans', 20)
font_big = pygame.font.SysFont('Lucida Sans', 24)



## Load Images
player_image = pygame.image.load('assets/jump.png').convert_alpha()
background_image = pygame.image.load('assets/background_image.png').convert_alpha()
box_image = pygame.image.load('assets/box.png').convert_alpha()



##### FUNCTIONS #####

## Output text to screen
def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    window.blit(img, (x,y))


## Drawing info Panel
def draw_panel():
    pygame.draw.rect(window, PANEL, (0, 0, WINDOW_WIDTH, 30))
    pygame.draw.line(window, WHITE, (0, 30), (WINDOW_WIDTH, 30), 2)
    draw_text('SCORE: ' + str(score), font_small, WHITE, 0, 0)



## Drawing Background
def draw_bg(bg_scroll):
    window.blit(background_image, (0, 0 + bg_scroll))
    window.blit(background_image, (0, -WINDOW_HEIGHT + bg_scroll))



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
    def __init__(self, x, y, width, moving):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(box_image, (width, 10))
        self.moving = moving
        self.move_counter = random.randint(0, 50)
        self.direction = random.choice([-1, 1])
        self.speed = random.choice([1, 2])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def update(self, scroll):
        ## Move box side to side if moving box
        if self.moving == True:
            self.move_counter += 1
            self.rect.x += self.direction * self.speed
        
        ## Change box direction if moved fully or hit wall
        if self.move_counter >= 100 or self.rect.left < 0 or self.rect.right > WINDOW_WIDTH:
            self.direction *= -1
            self.move_counter = 0
        

        ## Update box y pos
        self.rect.y += scroll

        ## See if Box off of screen
        if self.rect.top > WINDOW_HEIGHT:
            self.kill()



## -- Class Instances --
        
## Player Instance
player = Player(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 150)


## Box Instances Group
box_group = pygame.sprite.Group()

## Initial Box
box = Box(WINDOW_WIDTH // 2 - 25, WINDOW_HEIGHT - 50, 50, False)
box_group.add(box)



##### GAME #####

## Game Loop
run = True
while run:

    clock.tick(FPS)

    ## Game still playing (not over)
    if not game_over:
        scroll = player.move()

        ## Draw Background
        bg_scroll += scroll
        if bg_scroll >= WINDOW_HEIGHT:
            bg_scroll = 0
        draw_bg(bg_scroll)


        ## Generate Boxes
        if len(box_group) < MAX_BOXES:
            b_w = random.randint(40,60)
            b_x = random.randint(0, WINDOW_WIDTH - b_w)
            b_y = box.rect.y - random.randint(80, 120)
            b_type = random.randint(1,2)
            if b_type == 1 and score > 500:
                b_moving = True
            else:
                b_moving = False
            box = Box(b_x, b_y, b_w, b_moving)
            box_group.add(box)


        ## Update Boxes
        box_group.update(scroll)


        ## Update Score
        score += scroll


        ## Draw High Score line
        if high_score:
            pygame.draw.line(window, WHITE, (0, score - high_score + SCROLL_THRESH), (WINDOW_WIDTH, score - high_score + SCROLL_THRESH), 3)
            draw_text('HIGH SCORE', font_small, WHITE, WINDOW_WIDTH - 130, score - high_score + SCROLL_THRESH)

        ## Draw Panel
        draw_panel()


        ## Draw Sprites
        box_group.draw(window)
        player.draw()


        ## Check game over
        if player.rect.top > WINDOW_HEIGHT:
            game_over = True
    
    ## Game Over
    else:
        ## Fade Squares
        if fade_counter < WINDOW_WIDTH:
            fade_counter += 5
            fade_squares = 6
            for y in range(0, fade_squares, 2):
                pygame.draw.rect(window, BLACK, (0, y * (WINDOW_HEIGHT / fade_squares), fade_counter, WINDOW_HEIGHT / fade_squares))
                pygame.draw.rect(window, BLACK, (WINDOW_WIDTH - fade_counter, (y + 1) * (WINDOW_HEIGHT / fade_squares), WINDOW_WIDTH, WINDOW_HEIGHT / fade_squares))
        
        else:
            ## Game Over Text
            draw_text('GAME OVER', font_big, WHITE, 130, 200)
            draw_text('SCORE: ' + str(score), font_big, WHITE, 130, 250)
            draw_text('PRESS SPACE TO PLAY AGAIN', font_big, WHITE, 40, 300)
            
            ## Update High Score
            if score > high_score:
                high_score = score
                with open('score.txt', 'w') as file:
                    file.write(str(high_score))
            
            ## Wait for reset (space bar)
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE]:
                ## Reset Vars
                game_over = False
                score = 0
                scroll = 0
                fade_counter = 0
                ## Reposition Player
                player.rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 150)
                ## Reset Boxes
                box_group.empty()
                ## Initial Box
                box = Box(WINDOW_WIDTH // 2 - 25, WINDOW_HEIGHT - 50, 50, False)
                box_group.add(box)  



    ## Event Handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ## Update High Score
            if score > high_score:
                high_score = score
                with open('score.txt', 'w') as file:
                    file.write(str(high_score))
            run = False
    

    ## Update Display Window
    pygame.display.update()



pygame.quit()