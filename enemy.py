import pygame
import random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, WINDOW_WIDTH, y, sprite_sheet, scale):
        pygame.sprite.Sprite.__init__(self)

        ## Define Vars
        self.animation_list = []
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

        self.direction = random.choice([-1, 1])
        if self.direction == 1:
            self.flip = True
        else:
            self.flip = False

        ## Load images from spritesheet
        animation_steps = 6
        for animation in range(animation_steps):
            image = sprite_sheet.get_image(animation, 48, 48, scale, (0, 0, 0))
            image = pygame.transform.flip(image, self.flip, False)
            image.set_colorkey((0, 0, 0))
            self.animation_list.append(image)
        
        ## Select starting image and create rectangle
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()

        if self.direction == 1:
            self.rect.x = 0
        else:
            self.rect.x = WINDOW_WIDTH
        self.rect.y = y

    
    def update(self, scroll, WINDOW_WIDTH):
        ## Update Animation
        ANIMATION_COOLDOWN = 50
        
        ## Update image using current frame
        self.image = self.animation_list[self.frame_index]

        ## Check if enough time has passed
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        ## If last image, reset to start
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0


        ## Move Enemy
        self.rect.x += self.direction * 2
        self.rect.y += scroll

        ## Check if off window
        if self.rect.right < 0 or self.rect.left > WINDOW_WIDTH:
            self.kill()