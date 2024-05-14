#!/usr/bin/env python3

# Imports
import sys
from sys import exit
import pygame
import random
from random import randint, choice


# Initializing classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # In this section i am setting up the different images used for the animation of the character
        player_walk_1 = pygame.image.load(
            'runner_photos/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load(
            'runner_photos/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_jump = pygame.image.load(
            'runner_photos/player/player_jump.png').convert_alpha()
        self.player_index = 0

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(70, 425))
        self.gravity = 0

    # The player input function checks to see if the space bar has been hit and if so increases the height of the character allowing them to jump
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 425:
            self.gravity = -20

    # Apply gravity increases the gravity as the player is airborn giving the illusion of falling while also checking if the player has returned to the ground
    # and if not they recet them to the correct possition 425
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 425:
            self.rect.bottom = 425

    # Animation state checks to see if the player is jumping or above the bottom of their rectnagle and if so they change their animation to the jump animation
    def animation_state(self):
        if self.rect.bottom < 425:
            self.image = self.player_jump
        # If the player isnt jumping then they gradually change between the walking 1 and walking 2 images to give the illusion of movement and if the index reaches 1 it recets it
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]
    # Updating animpation, player input and gravity

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()


# Initiallization of the Obsticle class
class Obsticle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        # The type is sent by the python choice function taken from random and it is used to send either flame or blade to the obsticle function
        # as these are the two types of opticle used. it then sets up the pictures in a list similar to the player animation and changes between these images to make the
        # illusion of movement
        if type == 'flame':
            flame_frame1 = pygame.image.load(
                'runner_photos/flame/flame1.png').convert_alpha()
            flame_frame2 = pygame.image.load(
                'runner_photos/flame/flame2.png').convert_alpha()
            flame_frame3 = pygame.image.load(
                'runner_photos/flame/flame3.png').convert_alpha()
            self.frames = [flame_frame1, flame_frame2, flame_frame3]
            y_pos = 310
        else:
            blade_frame1 = pygame.image.load(
                'runner_photos/blade/blade1.png').convert_alpha()
            blade_frame2 = pygame.image.load(
                'runner_photos/blade/blade2.png').convert_alpha()
            self.frames = [blade_frame1, blade_frame2]
            y_pos = 420

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(
            midbottom=(random.randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 4
        self.destroy()
    # The destroy state is used to delete the item once it has gone of the screen

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


# This class is the same as the Obsticle class except it does not animate the backround items
class Backround(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == 'cload':
            cloud1 = pygame.image.load(
                'runner_photos/clouds1.png').convert_alpha()
            cloud2 = pygame.image.load(
                'runner_photos/clouds2.png').convert_alpha()
            cloud3 = pygame.image.load(
                'runner_photos/cloudsbaby.png').convert_alpha()
            self.frames = [cloud1, cloud2, cloud3]
            self.animation_index = random.randint(0, 2)
            y_pos = random.randint(80, 300)

        elif type == 'stone':
            rock1 = pygame.image.load(
                'runner_photos/large_stone.png').convert_alpha()
            rock2 = pygame.image.load(
                'runner_photos/Large_rock.png').convert_alpha()
            rock3 = pygame.image.load(
                'runner_photos/rocks.png').convert_alpha()
            self.frames = [rock1, rock2, rock3]
            self.animation_index = random.randint(0, 2)
            y_pos = 427

        elif type == 'floatingisland':
            island1 = pygame.image.load(
                'runner_photos/floating_island2.png').convert_alpha()
            island2 = pygame.image.load(
                'runner_photos/floating_island1.png').convert_alpha()
            self.frames = [island1, island2]
            self.animation_index = random.randint(0, 1)
            y_pos = random.randint(70, 200)

        elif type == 'tree':
            tree1 = pygame.image.load(
                'runner_photos/purple tree.png').convert_alpha()
            tree2 = pygame.image.load(
                'runner_photos/red tree.png').convert_alpha()
            self.frames = [tree1, tree2]
            self.animation_index = random.randint(0, 1)
            y_pos = 427

        else:
            gate = pygame.image.load('runner_photos/gate.png').convert_alpha()
            self.frames = [gate]
            self.animation_index = 0
            y_pos = 427

        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(
            midbottom=(random.randint(900, 1100), y_pos))

    def update(self):
        self.rect.x -= 4
        self.destroy()

    def destroy(self):
        if self.rect.x <= -150:
            self.kill()

# The collision_sprite checks to see if the player scrite has collided with the obsticle sprite and if it does it gives you a game over


def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True


def disply_score():
    current_time = int(pygame.time.get_ticks() // 1000) - start_time
    score_surface = test_font.render(
        f'Score:{(current_time)}', False, (64, 64, 64))
    score_rect = score_surface.get_rect(center=(450, 50))
    screen.blit(score_surface, score_rect)
    return current_time


# Initiallizing the pygame class and other important informamtion
pygame.init()
screen = pygame.display.set_mode((900, 500))
pygame.display.set_caption('Runner')
Clock = pygame.time.Clock()

# Creating the sky, ground and font surface for the game
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)

ground_surface = pygame.image.load('runner_photos/ground.png').convert()

sky_surface = pygame.image.load('runner_photos/sky.png').convert()
# Setting up the player surfaces and rectangles
player_stand = pygame.image.load(
    'runner_photos/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.scale2x(player_stand)
player_stand_rect = player_stand.get_rect(center=(450, 250))
start_time = 0
score = 0

# Setting up the sprites for each item so they can be manipulatedmore easily
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

backround_group = pygame.sprite.Group()

# Timers, these timers are used to determine how often obstacles and backround items spawn as well as how quickly the animation for each item runs
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1543)

blade_animataion_timer = pygame.USEREVENT + 2
pygame.time.set_timer(blade_animataion_timer, 200)

flame_animataion_timer = pygame.USEREVENT + 3
pygame.time.set_timer(flame_animataion_timer, 100)

backround_timer = pygame.USEREVENT + 4
pygame.time.set_timer(backround_timer, 5000)

# This is just setting up the rectangles for the text on the home screen
game_name = test_font.render('Runner', False, (111, 196, 169))
game_name_rect = game_name.get_rect(center=(450, 130))
game_instructions = test_font.render(
    'Press Space to run', False, (111, 196, 169))
game_instructions_rect = game_instructions.get_rect(center=(450, 370))

# Setting the game to inactive so that the home screen will appear first
game_active = False

# The game will continue to run while this while loop is active
while True:
    # This for loop checks to see if you have pressed the x on the top right of the screen and if you do it will end the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        # This if statement is in case the game is inactive (on the home or the game over screen) this allows the user to press space and try again
        if game_active == False:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = True
                    start_time = int(pygame.time.get_ticks() // 1000)

        # This if statement is used to create the sprite obstacles if the game is active
        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(
                    Obsticle(choice(['blade', 'blade', 'flame', 'blade'])))

        # This if statement is used to create harmless backround items if the game is active
        if game_active:
            if event.type == backround_timer:
                backround_group.add(
                    Backround(choice(['cloud', 'floatingisland', 'gate', 'stone', 'tree'])))

    # Checking if game is actiive and if so creating the backround, player and obsticals
    if game_active:
        # These are backround items
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 0))
        # The display score function return the score as well as using a surface to display the current score in seconds
        score = disply_score()
        disply_score()

        # This creates backround items such as gates, trees, floating islands and other items which do not harm the play
        backround_group.draw(screen)
        backround_group.update()

        # This creates the player as well as the animamtion for the player while they are displayed on screen
        player.draw(screen)
        player.update()

        # This section creates the obstacles that the player has to avoid
        obstacle_group.draw(screen)
        obstacle_group.update()

        # collision, the collision function checks to see if the player collides with an obsticle and if so it causes the game_active function to become false thus giving a game over
        game_active = collision_sprite()

    # This else statement only runs if the game_active variable is False this happens when the game starts and it occurs when the player gets a game over by hitting an obstacle
    # The game_active can be turned to true by pressing the space key and this will begin the game
    else:
        # The screen fill, makes a nice blue blackround for the starting screen
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        score_message = test_font.render(
            f'Your Score: {score}', False, (11, 196, 169))
        score_message_rect = score_message.get_rect(center=(450, 370))
        screen.blit(game_name, game_name_rect)

        # The if statement checks to see if the game is starting up or if you have lost a game if you lost a game it will diplay your last score
        # if you are starting up it will display instructions on how to start the game
        if score == 0:
            screen.blit(game_instructions, game_instructions_rect)
        else:
            screen.blit(score_message, score_message_rect)

    # This function updates the screen/display
    pygame.display.update()
    # This is the fps
    Clock.tick(60)
