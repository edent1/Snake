import pygame
import random
import tkinter as tk
from tkinter import messagebox

pygame.init()

def redrawWindow(surface):
    global rows, width,snake,food
    surface.fill((0,0,0))
    snake.draw(surface)
    food.draw(surface)
    drawGrid(width,rows,surface)
    pygame.display.update()

def drawGrid(w,rows,surface):
    sizeBetween = w // rows
    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBetween
        y = y + sizeBetween
        pygame.draw.line(surface, (255,255,255), (x,0) , (x,w))
        pygame.draw.line(surface, (255,255,255), (0,y) , (w,y))

def randomFood(rows,item):
    position = item.body
    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z:z.pos == (x,y),position))) > 0 :
            continue
        else:
            break
    return(x,y)

def message(subject,content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject,content)
    try:
        root.destroy()
    except:
        pass

class snake(object):
    body = []
    turns = {}
    def __init__(self,colour,pos):
        self.colour = colour
        self.head = cube(pos)
        self.body.append(self.head)
        self.xvel = 0
        self.yvel = 0

    def move(self):
        keys = pygame.key.get_pressed()
        for key in keys:
            if keys[pygame.K_LEFT]:
                self.xvel = -1
                self.yvel = 0
                self.turns[self.head.pos[:]] = [self.xvel, self.yvel]
            elif keys[pygame.K_RIGHT]:
                self.xvel = 1
                self.yvel = 0
                self.turns[self.head.pos[:]] = [self.xvel, self.yvel]
            elif keys[pygame.K_UP]:
                self.yvel = -1
                self.xvel = 0
                self.turns[self.head.pos[:]] = [self.xvel, self.yvel]
            elif keys[pygame.K_DOWN]:
                self.yvel = 1
                self.xvel = 0
                self.turns[self.head.pos[:]] = [self.xvel, self.yvel]

        for i, c in enumerate(self.body) :
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0],turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)
            else:
                if c.xvel == -1 and c.pos[0] <= 0:
                    death()
                elif c.xvel == 1 and c.pos[0] >= c.rows -1:
                    death()
                elif c.yvel == -1 and c.pos[1] <= 0:
                    death()
                elif c.yvel == -1 and c.pos[1] >= c.rows -1:
                    death()
                else:
                    c.move(c.xvel,c.yvel)

    def draw(self,surface):
        for i, c in enumerate(self.body):
             c.draw(surface)

    def addCube(self):
        tail = self.body[-1]
        xdirection = tail.xvel
        ydirection = tail.yvel
        if xdirection == 1 and ydirection == 0:
            self.body.append(cube((tail.pos[0]-1,tail.pos[1] )))
        if xdirection == -1 and ydirection == 0:
            self.body.append(cube((tail.pos[0] + 1, tail.pos[1] )))
        if xdirection == 0 and ydirection == 1:
            self.body.append(cube((tail.pos[0] , tail.pos[1]-1 )))
        if xdirection == 0 and ydirection == -1:
            self.body.append(cube((tail.pos[0] , tail.pos[1] +1 )))
        self.body[-1].xvel = xdirection
        self.body[-1].yvel = ydirection

    def reset(self,pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.xvel = 0
        self.yvel = 0

class cube(object):
    rows = 20
    width = 500
    def __init__(self,start,xvel=0,yvel=0,colour = (255,0,0)):
        self.pos = start
        self.xvel = xvel
        self.yvel = yvel
        self.colour = colour

    def move(self,xvel,yvel):
        self.xvel = xvel
        self.yvel = yvel
        self.pos = (self.pos[0] + self.xvel, self.pos[1] + self.yvel)

    def draw(self,surface):
        distance = self.width // self.rows
        i = self.pos[0] #rows
        j = self.pos[1] #cols
        pygame.draw.rect(surface, self.colour, (i*distance+1,j*distance+1,distance - 2, distance - 2))

def death():
    for x in range(len(snake.body)):
        if snake.body[x].pos in list(map(lambda x: x.pos, snake.body[x + 1:])):
            print('Score: ', len(snake.body))
            message('Game Over!', 'Please play again!')
            snake.reset((10, 10))
            break
def main():
    global rows,width,snake,food
    run = True
    width = 500
    rows = 20
    window = pygame.display.set_mode((width,width))
    pygame.display.set_caption("Snake")
    clock = pygame.time.Clock()
    snake = snake((255, 255, 0), (10, 10))
    food = cube(randomFood(rows,snake), colour=(255,0,255))

    while run:
        pygame.event.get()
        pygame.time.delay(50)
        clock.tick(10)
        snake.move()
        if snake.body[0].pos == food.pos:
            snake.addCube()
            food = cube(randomFood(rows,snake), colour=(255,0,255))
        redrawWindow(window)
        death()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                pygame.quit()
                exit()

main()