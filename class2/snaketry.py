import pygame as pg
import time

pg.init()
w= 12
h= 8
L = 50
pad =5
toppad = 30

screen = pg.display.set_mode((w*L,h*L+toppad))

default_font = pg.font.get_default_font()
font = pg.font.SysFont(default_font, 30)

snake = []

snake.append((h,0))
direction = "up"

point_pos = (h//2,w//2)


running = True
while running:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
            elif event.key == pg.K_UP:
                direction = "up"
            elif event.key == pg.K_DOWN:
                direction = "down"
            elif event.key == pg.K_LEFT:
                direction = "left"
            elif event.key == pg.K_RIGHT:
                direction = "right"
        
    #update snake
    head_row,head_col = snake[0]
    print(head_row)
    print(head_col)

    if direction == "up":
        new_head = (head_row-1,head_col)
    elif direction == "right":
        new_head = (head_row,head_col+1)
    if direction == "down":
        new_head = (head_row+1,head_col)
    if direction == "left":
        new_head = (head_row,head_col-1)

    snake.insert(0,new_head)
    print(snake)
    snake.pop()
    print(snake)

    #draw game board
    for col in range(0,w):
        for row in range(0,h):
            pg.draw.rect(screen,(50,50,50), pg.Rect(col*L+pad,row*L+pad+toppad,L-pad,L-pad))

    #draw snake
    for s in snake:
        row,col = s
        pg.draw.rect(screen,(200,200,200),pg.Rect(col*L+pad,row*L+pad+toppad,L-pad,L-pad))

    text = font.render('Snake', True, (220,220,220))
    screen.blit(text, (5,5))

    if snake[0] == point_pos:
        snake.append(point_pos)


    pg.draw.rect(screen, (200,20,20), pg.Rect(point_pos[1]*L+pad,point_pos[0]*L+pad+toppad,L-pad,L-pad))

    pg.display.flip()

    time.sleep(0.2)