### Citations ###
# some content from kids can code: http://kidscancode.org/blog/ (collision, movement, sprites)
# sprites from https://opengameart.org/content/space-shooter-redux
# my dad helped with some movement logic and helped fix movement bugs
'''
My final project is the snake game
'''


# import external libraries and modules
import pygame as pg
from pygame.sprite import Sprite
# import built in libraries
import random
from os import path
# import created libraries
from settings import *


# vectors
vec = pg.math.Vector2

# init pygame and create a window
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Snake by Andrew Perevoztchikov")
clock = pg.time.Clock()

hiscore = open("game\hiscore.txt", "r+")
hiscore_print = int(hiscore.read())


# loading filepaths for the sprite images
# img_dir1 = path.join(path.dirname(__file__), r'C:\githubstuff\intro_to_programming\videogameFall2022\game\images')

# function to draw text on the screen
def draw_text(text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        screen.blit(text_surface, text_rect)

# random color generator
def colorbyte():
    return random.randint(0,255)

# get images for sprites and assign to variables
# background = pg.image.load(path.join(img_dir1, 'black.png')).convert()
# background = pg.transform.scale(background, (WIDTH, HEIGHT))
# background_rect = background.get_rect()
# player_img = pg.image.load(path.join(img_dir1, "playerShip1_orange.png")).convert()
# enemy_img = pg.image.load(path.join(img_dir1, "enemyGreen3.png")).convert()
# bullet_img = pg.image.load(path.join(img_dir1, "laserRed16.png")).convert()
# boss_img = pg.image.load(path.join(img_dir1, "enemyBlue2.png")).convert()

# this list is very important as it stores all data for each snake segment in an easily accessible indexed list
snake_segments = []
snake_segments2 = []
apple_list = []
wall_list = []
index = 1
index2 = 1

# xdir = random.choice(["left", "right"])
# ydir = random.choice(["up", "down"])

# variables for coordinates of new spawned segment after apple is eaten      
spawnx = 0 
spawny = 0    

count = 1
direction = 0
# snake class for initializing individual segments of the snake
class Snake_Segment(Sprite):
    def __init__(self, type, index, x, y, direction, player):
        Sprite.__init__(self)
        self.image = pg.Surface((20, 20))
        if player == "p1":
            self.image.fill(GREEN)
        if player == "p2":
            self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = SNAKE_SPEED
        self.direction = direction
        self.type = type
        self.index = index
        self.next_direction = ""
        self.change_direction = False
        self.no_update = False
        self.ai = False
        self.x = x
        self.y = y
        self.player = player
    def controls(self):
        global direction, SAFETY_FRAMES
        keys = pg.key.get_pressed()
        # sets initial key press to outside variable so that multiple keypressess will not be registered before updating snake
        if self.player == "p1":
            if keys[pg.K_LEFT]:
                direction = 1
            if keys[pg.K_RIGHT]:
                direction = 2
            if keys[pg.K_UP]:
                direction = 3
            if keys[pg.K_DOWN]:
                direction = 4
        if self.player == "p2":
            if keys[pg.K_a]:
                direction = 5
            if keys[pg.K_d]:
                direction = 6
            if keys[pg.K_w]:
                direction = 7
            if keys[pg.K_s]:
                direction = 8
        
        
        # code for head movement
        if self.type == "head":
            # new movement direction
            # limits direction changes to only when snake movement will be updated
            if self.ai == False:
                if FRAME % SNAKE_SPEED == 0:
                    if self.player == "p1":
                        if direction == 1:
                            #  all of the != blocks make sure snake will not go back into itself             
                            if self.direction != "right":
                                self.direction = "left"                  
                                
                        if direction == 2:                  
                            if self.direction != "left":
                                self.direction = "right"
                                                
                        if direction == 3:                
                            if self.direction != "down":
                                self.direction = "up"
                                            
                        if direction == 4:                 
                            if self.direction != "up":
                                self.direction = "down"
                    if self.player == "p2":
                        if direction == 5:
                            #  all of the != blocks make sure snake will not go back into itself             
                            if self.direction != "right":
                                self.direction = "left"                  
                                
                        if direction == 6:                  
                            if self.direction != "left":
                                self.direction = "right"
                                                
                        if direction == 7:                
                            if self.direction != "down":
                                self.direction = "up"
                                            
                        if direction == 8:                 
                            if self.direction != "up":
                                self.direction = "down"
            
            # automatic movement function
            if self.ai == True:               
                if FRAME % SNAKE_SPEED == 0:
                    # code to prevent snake from hitting its own tail
                    for segment in snake_segments[1:]:
                        if self.rect.x == segment.rect.x:
                            # checks direction of head and checks if it is about to collide with the tail and makes it move parallel thus avoiding tail
                            if self.direction == "up": 
                                if (self.rect.y - segment.rect.y)/20 == 1 or (self.rect.y - segment.rect.y)/20 == 2:
                                    self.direction = random.choice(["left", "right"])
                                    SAFETY_FRAMES += SNAKE_SPEED * 20
                            elif self.direction == "down":
                                if (self.rect.y - segment.rect.y)/20 == -1 or (self.rect.y - segment.rect.y)/20 == -2:
                                    self.direction = random.choice(["left", "right"])
                                    SAFETY_FRAMES += SNAKE_SPEED * 20

                        elif self.rect.y == segment.rect.y:
                            if self.direction == "right": 
                                if (self.rect.x - segment.rect.x)/20 == -1 or (self.rect.x - segment.rect.x)/20 == -2:
                                    self.direction = random.choice(["up", "down"])
                                    SAFETY_FRAMES += SNAKE_SPEED * 20
                            elif self.direction == "left":
                                if (self.rect.x - segment.rect.x)/20 == 1 or (self.rect.x - segment.rect.x)/20 == 2:
                                    self.direction = random.choice(["up", "down"])
                                    SAFETY_FRAMES += SNAKE_SPEED * 10
                                    
                    for segment in wall_list:
                        if self.rect.x == segment.rect.x:
                            # checks direction of head and checks if it is about to collide with the tail and makes it move parallel thus avoiding tail
                            if self.direction == "up": 
                                if (self.rect.y - segment.rect.y)/20 == 1 or (self.rect.y - segment.rect.y)/20 == 2:
                                    self.direction = random.choice(["left", "right"])
                                    SAFETY_FRAMES += SNAKE_SPEED * 10
                            elif self.direction == "down":
                                if (self.rect.y - segment.rect.y)/20 == -1 or (self.rect.y - segment.rect.y)/20 == -2:
                                    self.direction = random.choice(["left", "right"])
                                    SAFETY_FRAMES += SNAKE_SPEED * 10

                        elif self.rect.y == segment.rect.y:
                            if self.direction == "right": 
                                if (self.rect.x - segment.rect.x)/20 == -1 or (self.rect.x - segment.rect.x)/20 == -2:
                                    self.direction = random.choice(["up", "down"])
                                    SAFETY_FRAMES += SNAKE_SPEED * 10
                            elif self.direction == "left":
                                if (self.rect.x - segment.rect.x)/20 == 1 or (self.rect.x - segment.rect.x)/20 == 2:
                                    self.direction = random.choice(["up", "down"])
                                    SAFETY_FRAMES += SNAKE_SPEED * 10
                    
                    if SAFETY_FRAMES == 0:   
                        if self.rect.x == apple_list[0].rect.x:
                            if apple_list[0].rect.y < self.rect.y:                         
                                if self.direction != "down":
                                    self.direction = "up"
                            if apple_list[0].rect.y > self.rect.y: 
                                if self.direction != "up": 
                                    self.direction = "down"
                        if self.rect.y == apple_list[0].rect.y:
                            if apple_list[0].rect.x < self.rect.x: 
                                if self.direction != "right":
                                    self.direction = "left"
                            if apple_list[0].rect.x > self.rect.x: 
                                if self.direction != "left":
                                    self.direction = "right"
                    
    def update(self):
        global LIVES, SPAWN_QUEUE, spawnx, spawny, MAX_LEN, index
        self.controls()
        
        if self.player == "p1":
            # if direction is already set
            if FRAME % SNAKE_SPEED == 0:
                # movement instructions for the body segments
                if self.type == "body":
                    # if change_direction is true then the segment of the snake will be allowed to change direction to the below queued direction
                    if self.change_direction == True:
                        self.direction = snake_segments[self.index - 1].direction
                        self.direction = self.next_direction
                        self.change_direction = False
                    # this statement checks if the snake segment in front of the current one has changed direction
                    # next_direction queues the direction of the snake segment in front of the current one but does not change direction just yet so that the current segment can catch up with the one in front of it and not cause gaps
                    # this block then allows change_direction to be true so that in the next update the segment can change direction
                    if self.direction != snake_segments[self.index - 1].direction:
                        self.next_direction = snake_segments[self.index - 1].direction
                        self.change_direction = True
                # this is just code to actually move the segment in the right direction by its width/hight(which is 20)
                if self.direction == "left":                
                    self.rect.x -= 20
                if self.direction == "right":                           
                    self.rect.x += 20           
                if self.direction == "up":                           
                    self.rect.y -= 20           
                if self.direction == "down":                           
                    self.rect.y += 20
        if self.player == "p2":
            # if direction is already set
            if FRAME % SNAKE_SPEED == 0:
                # movement instructions for the body segments
                if self.type == "body":
                    # if change_direction is true then the segment of the snake will be allowed to change direction to the below queued direction
                    if self.change_direction == True:
                        self.direction = snake_segments2[self.index - 1].direction
                        self.direction = self.next_direction
                        self.change_direction = False
                    # this statement checks if the snake segment in front of the current one has changed direction
                    # next_direction queues the direction of the snake segment in front of the current one but does not change direction just yet so that the current segment can catch up with the one in front of it and not cause gaps
                    # this block then allows change_direction to be true so that in the next update the segment can change direction
                    if self.direction != snake_segments2[self.index - 1].direction:
                        self.next_direction = snake_segments2[self.index - 1].direction
                        self.change_direction = True
                # this is just code to actually move the segment in the right direction by its width/hight(which is 20)
                if self.direction == "left":                
                    self.rect.x -= 20
                if self.direction == "right":                           
                    self.rect.x += 20           
                if self.direction == "up":                           
                    self.rect.y -= 20           
                if self.direction == "down":                           
                    self.rect.y += 20
        
        
        # this allows the snake to pass through the screen border and appear on the other side
        if self.rect.x < 0:
            self.rect.x = WIDTH - 20
        elif self.rect.x > WIDTH:
            self.rect.x = 0
        elif self.rect.y < 0:
            self.rect.y = HEIGHT - 20
        elif self.rect.y > HEIGHT:
            self.rect.y = 0
            
        
          
# apple class
class Apple(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        self.image = pg.Surface((20, 20))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
    def update(self):
        global SCORE, index, spawnx, spawny, SNAKE_SPEED, LEVEL, xdir, ydir, SPAWN_QUEUE, LENGTH_PER_APPLE, SPAWN_QUEUE2
        # checks for apple collision with the snake
        hits = pg.sprite.spritecollide(self, snake, False)
        if hits:
            if hits[0].type == "head":
                if hits[0].player == "p1":
                    SPAWN_QUEUE += LENGTH_PER_APPLE
                    # adds one to score and kills apple    
                    SCORE += 1
                    # levels that progress in difficulty
                    if SNAKE_SPEED > 3:
                        if LEVEL * 5 - SCORE == 0:
                            SNAKE_SPEED -= 1
                            LEVEL += 1
                    # xdir = random.choice(["left", "right"])
                    # ydir = random.choice(["up", "down"])
                    apple_list.remove(self)
                    self.kill()
                if hits[0].player == "p2":
                    SPAWN_QUEUE2 += LENGTH_PER_APPLE
                    # adds one to score and kills apple    
                    SCORE += 1
                    # levels that progress in difficulty
                    if SNAKE_SPEED > 3:
                        if LEVEL * 5 - SCORE == 0:
                            SNAKE_SPEED -= 1
                            LEVEL += 1
                    # xdir = random.choice(["left", "right"])
                    # ydir = random.choice(["up", "down"])
                    apple_list.remove(self)
                    self.kill()
            else: 
                apple_list.remove(self)
                self.kill()
        
        hits1 = pg.sprite.spritecollide(self, walls, False)
        if hits1:
            apple_list.remove(self)
            self.kill()

class Wall(Sprite):
    def __init__(self, x, y, iterations):
        Sprite.__init__(self)
        self.image = pg.Surface((20, 20))
        self.image.fill(GREY)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.x = x
        self.y = y
        self.iterations = iterations
        self.direction = ""
    
    def update(self):
        global LIVES
        # variables for x and y of previous wall
        prevx = self.x
        prevy = self.y
        x = self.x
        y = self.y
        # count to make sure walls dont turn too often
        count = 0
        if self.iterations == 1:
            for i in range(WALL_LEN):
                # variable to store direction of previous wall for later calculations
                old_direction = self.direction
                
                # at every turn of the wall it will choose a random direction that is not going back into the wall
                if self.direction == "left":
                    self.direction = random.choice(["right", "up", "down"])
                elif self.direction == "right":
                    self.direction = random.choice(["left", "up", "down"])
                elif self.direction == "up":
                    self.direction = random.choice(["left", "right", "down"])
                elif self.direction == "down":
                    self.direction = random.choice(["left", "right", "up"])
                else:
                    self.direction = random.choice(["left", "right", "up", "down"])
                
                # makes sure wall doesnt turn too often
                if self.direction != old_direction:
                    if count % 3 != 0:
                        self.direction = old_direction
                
                # creates new wall based off direction
                if self.direction == "left":                
                    x = prevx - 20
                if self.direction == "right":                           
                    x = prevx + 20           
                if self.direction == "up":                           
                    y = prevy - 20           
                if self.direction == "down":                           
                    y = prevy + 20
                prevx = x
                prevy = y
                wall = Wall(x, y, 0)
                wall_list.append(wall)
                walls.add(wall)
                all_sprites.add(wall)
                count += 1
            self.kill()
        
        hits = pg.sprite.spritecollide(self, snake, False)
        if hits:
            if hits[0].type == "head":
                LIVES -= 1
        

# create a group for all sprites
all_sprites = pg.sprite.Group()
apples = pg.sprite.Group()
snake = pg.sprite.Group()
walls = pg.sprite.Group()


# initialises snake head before anything else for simplicity
snake_head = Snake_Segment("head", 0, WIDTH/2 + 10, HEIGHT/2 + 10, "right", "p1")
all_sprites.add(snake_head)
snake.add(snake_head)
snake_segments.append(snake_head)

if MULTIPLAYER == True:
    # initialises snake head before anything else for simplicity
    snake_head2 = Snake_Segment("head", 0, WIDTH/2 + 10 - 40, HEIGHT/2 + 10, "left", "p2")
    all_sprites.add(snake_head2)
    snake.add(snake_head2)
    snake_segments2.append(snake_head2)

 
if WALLS == True:  
    for i in range(AMOUNT_WALLS): 
        x = random.randint(1, WIDTH/20 - 2) * 20 + 10
        y = random.randint(1, HEIGHT/20 - 2) * 20 + 10
        if abs(x - snake_head.rect.x) >= 20:
            if abs(y - snake_head.rect.y) >= 20:           
                wall = Wall(x, y, 1)
                wall_list.append(wall)
                walls.add(wall)
                all_sprites.add(wall)
        if abs(y - snake_head.rect.y) >= 20:
            if abs(x - snake_head.rect.x) >= 20:           
                wall = Wall(x, y, 1)
                wall_list.append(wall)
                walls.add(wall)
                all_sprites.add(wall)

# win = False
# Game loop
running = True
gameover = False
pause = False
press = 1
win = False
while running:
    # keep the loop running using clock
    clock.tick(FPS)

    # get pygame events to check
    for event in pg.event.get():
        # check for closed window
        if event.type == pg.QUIT:
            running = False
        
        # checks if key to pause game has been pressed
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_p:
                if press % 2 == 0:
                    pause = False
                else:
                    pause = True       
                press += 1  
     

    
    # code to spawn in new snake segments when collision with apple is detected.
    if FRAME % SNAKE_SPEED == 0:
        if SPAWN_QUEUE != 0:
            if len(snake_segments) <= MAX_LEN:
                # checks the direction of the last segment of the snake to provide coordinates for spawining in the new segment
                if snake_segments[len(snake_segments) - 1].direction == "left":
                    spawnx = 20
                if snake_segments[len(snake_segments) - 1].direction == "right":
                    spawnx = -20
                if snake_segments[len(snake_segments) - 1].direction == "up":
                    spawny = 20
                if snake_segments[len(snake_segments) - 1].direction == "down":
                    spawny = -20
                # print(spawnx, ",", spawny)
                # spawns in the new segment with the correct coordinates and same direction as the last segment
                segment = Snake_Segment("body", index, (snake_segments[index - 1].rect.center[0] + spawnx), (snake_segments[index - 1].rect.center[1]) + spawny, snake_segments[len(snake_segments) - 1].direction, "p1")
                # adds segment to all the sprite groups and the indexed list of snake segments
                all_sprites.add(segment)
                snake.add(segment)
                snake_segments.append(segment)
                index += 1
                # resets the coordinates for the next run to avoid conflicts
                spawnx = 0 
                spawny = 0
                SPAWN_QUEUE -= 1
        if SPAWN_QUEUE2 != 0:
            if len(snake_segments2) <= MAX_LEN:
                # checks the direction of the last segment of the snake to provide coordinates for spawining in the new segment
                if snake_segments2[len(snake_segments2) - 1].direction == "left":
                    spawnx = 20
                if snake_segments2[len(snake_segments2) - 1].direction == "right":
                    spawnx = -20
                if snake_segments2[len(snake_segments2) - 1].direction == "up":
                    spawny = 20
                if snake_segments2[len(snake_segments2) - 1].direction == "down":
                    spawny = -20
                # print(spawnx, ",", spawny)
                # spawns in the new segment with the correct coordinates and same direction as the last segment
                segment = Snake_Segment("body", index2, (snake_segments2[index2 - 1].rect.center[0] + spawnx), (snake_segments2[index2 - 1].rect.center[1]) + spawny, snake_segments2[len(snake_segments2) - 1].direction, "p2")
                # adds segment to all the sprite groups and the indexed list of snake segments
                all_sprites.add(segment)
                snake.add(segment)
                snake_segments2.append(segment)
                index2 += 1
                # resets the coordinates for the next run to avoid conflicts
                spawnx = 0 
                spawny = 0
                SPAWN_QUEUE2 -= 1
                
    
    # spawns new apple at random coordinates when the previous one is eaten
    if len(apples) <= APPLE_AMOUNT:
        x = random.randint(0, WIDTH/20 - 1) * 20 + 10
        y = random.randint(0, HEIGHT/20 - 1) * 20 + 10
        apple = Apple(x, y)
        apples.add(apple)
        all_sprites.add(apple)
        apple_list.append(apple)
    
        
    print(len(walls))   
    
    ############ Draw ################
    # draw the background screen
    screen.fill(BLACK)
    # screen.blit(background, background_rect)
    # draw all sprites
    all_sprites.draw(screen)

    if MULTIPLAYER == False:
        # checks if the snake's head collides with the body and subtracts one life
        hits = pg.sprite.spritecollide(snake_head, snake, False)
        if len(hits) == 2:
            LIVES -= 1
    else:
        hits = pg.sprite.spritecollide(snake_head, snake, False)
        hits1 = pg.sprite.spritecollide(snake_head2, snake, False)
        if len(hits) == 2:
            if hits[1].player == "p2":
                draw_text("PLAYER 2 WINS", 144, BLUE, WIDTH / 2, HEIGHT / 2)
                win = True
        if len(hits1) == 2:
            if hits1[1].player == "p1":
                draw_text("PLAYER 1 WINS", 144, GREEN, WIDTH / 2, HEIGHT / 2)
                win = True
                
        
    
    ############ Update ##############
    # update all sprites
    # for segment in snake_segments:
    #     segment.update()
    if MULTIPLAYER == False:
        # updates sprites while game is not over or paused
        if gameover == False and pause == False:
            all_sprites.update()
    else:
        if win != True:
            all_sprites.update()
        
    # if FRAME % SNAKE_SPEED == 0:
    #     count += 1
    if SAFETY_FRAMES > 0:
        SAFETY_FRAMES -= 1
    
    
    # draw score and lives on screen
    draw_text("POINTS: " + str(SCORE), 22, WHITE, WIDTH / 2, HEIGHT / 24)
    draw_text("LIVES: " + str(LIVES), 22, WHITE, WIDTH / 2 - 100, HEIGHT / 24)
    # draw_text("FRAMES: " + str(FRAME), 22, WHITE, WIDTH / 2 + 150, HEIGHT / 24)
    draw_text("LEVEL: " + str(LEVEL), 22, WHITE, WIDTH / 2 + 300, HEIGHT / 24)
    draw_text("PRESS 'P' TO PAUSE", 22, WHITE, WIDTH / 2 - 250, HEIGHT / 24)
    draw_text("SNAKE LENGTH: " + str(len(snake)), 22, WHITE, WIDTH / 2 - 450, HEIGHT / 24)
    draw_text("HISCORE: " + str(hiscore_print), 22, WHITE, WIDTH / 2 + 450, HEIGHT / 24)
    if pause == True:
        draw_text("GAME PAUSED", 144, WHITE, WIDTH / 2, HEIGHT / 2)
    
        
    # check if you lose
    if LIVES <= 0:    
        draw_text("GAME OVER", 144, RED, WIDTH / 2, HEIGHT / 2)
        gameover = True

    # buffer - after drawing everything, flip display
    pg.display.flip()
    FRAME += 1

if SCORE > hiscore_print:
    hiscore.seek(0)
    hiscore.write(str(SCORE))
hiscore.close()
pg.quit()
