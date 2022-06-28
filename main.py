from tkinter import Grid
import pygame
import sys
import random

#create class Snake with length of 1, positions of body(array), direction, color(RGB) and score set to 0
class Snake(object):
    def __init__(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = (17, 24, 47)
        self.score = 0

    #get position of head, first box in array of positions
    def get_head_position(self):
        return self.positions[0]
    
    #change the direction of the snake
    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point
    
    #move the snake
    def move(self):
        #curr is the position of the head
        curr = self.get_head_position()

        #x, y is the direction of movement
        x, y = self.direction

        #new is a new box added to the snake
        new = (((curr[0] + (x*GRIDSIZE)) % SCREEN_WIDTH), (curr[1] + (y*GRIDSIZE)) % SCREEN_HEIGHT)

        #if the length of the snake is more than 3(0,1,2) and the new box hits any of the positions then reset
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        else:
            #add the new box to the length of the snake at head position
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()
   
    #reset snake
    def reset(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT /2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0

    #draw the snake
    def draw(self, surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (GRIDSIZE, GRIDSIZE))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, (93, 216, 228), r, 1)

    #turn the snake if UP, DOWN, LEFT or RIGHT keys are hit
    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(UP)
                elif event.key == pygame.K_DOWN:
                    self.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.turn(RIGHT)

#create class food with a position and color and a function to randomize position
class Food(object):
    def __init__(self):
        self.position = (0, 0)
        self.color = (223, 163, 49)
        self.randomize_position()

    #randomize position of food function
    def randomize_position(self):
        self.position = (random.randint(0, GRIDWIDTH -1) * GRIDSIZE, random.randint(0, GRIDHEIGHT -1) * GRIDSIZE)

    #draw the food
    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (GRIDSIZE, GRIDSIZE))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, (93, 216, 228), r, 1)

#function to draw the game area grid
def drawGrid(surface):
    for y in range(0, int(GRIDHEIGHT)):
        for x in range(0, int(GRIDWIDTH)):
            if(x + y) % 2 == 0:
                r = pygame.Rect((x*GRIDSIZE, y*GRIDSIZE), (GRIDSIZE, GRIDSIZE))
                pygame.draw.rect(surface, (93, 216, 228), r)
            else:
                r = pygame.Rect((x*GRIDSIZE, y*GRIDSIZE), (GRIDSIZE, GRIDSIZE))
                pygame.draw.rect(surface, (84, 194, 205), r)
                

#variable to set screen size in pixels
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 480

#size of each box in grid in pixels
GRIDSIZE = 20
GRIDWIDTH = SCREEN_WIDTH / GRIDSIZE
GRIDHEIGHT = SCREEN_HEIGHT / GRIDSIZE

#up x = 0, y = -1
UP = (0, -1)
#down x = 0, y = 1
DOWN = (0, 1)
#left x = -1, y = 0
LEFT = (-1, 0)
#right x = 1, y = 0
RIGHT = (1, 0)

#main function
def main():
    #initialize the game
    pygame.init()

    #game clock keeps track of action at all times
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

    #surface or game are grid is drawn
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    drawGrid(surface)

    #initialize snake class
    snake = Snake()
    #initialize food class
    food = Food()
    #create a font variable
    myfont = pygame.font.SysFont('monospace', 16)
    
    #game loop runs forever
    while(True):
        #clock used to determine game speed
        clock.tick(10)

        snake.handle_keys()
        drawGrid(surface)
        snake.move()
        if snake.get_head_position() == food.position:
            snake.length += 1
            snake.score += 1
            food.randomize_position()
        snake.draw(surface)
        food.draw(surface)
 
        screen.blit(surface, (0, 0))
        text = myfont.render('Score {0}'.format(snake.score), 1, (0, 0, 0))
        screen.blit(text, (5, 10))
        pygame.display.update()
main()