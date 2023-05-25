import numpy as np
import pygame
import sys
from block import gamemenager,Block
from math import trunc


SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
PIXEL_WIDTH = 7
PIXEL_HEIGHT = 7
RENDERSIZEX = 200
RENDERSIZEY = 200
MARGINX = 0
MARGINY = 0
FPS = 9999
STARTERBRUSHSIZE = 2
BRUSHSIZELIMIT = 10
STARTERINVSLOT = 1


pygame.init()
pygame.font.init()
main_clock = pygame.time.Clock()
game =  gamemenager('block game',SCREEN_WIDTH, SCREEN_HEIGHT,RENDERSIZEX,RENDERSIZEY)
brush_size = STARTERBRUSHSIZE
game.set_up()

air = Block("air",game,gamemenager.blue_sky,game.blocktype[2],0)
wood = Block("wood",game,gamemenager.brown,game.blocktype[0],99)
stone = Block("stone",game,gamemenager.stone_gray,game.blocktype[0],99)
water = Block("water",game,gamemenager.blue,game.blocktype[1],3)
oil = Block("oil",game,gamemenager.yellow,game.blocktype[1],2)
STARTERCLICKBLOCK = wood
inventory = [air,wood,stone,water,oil]
current_block = STARTERCLICKBLOCK
inventory_slot = STARTERINVSLOT

game.create_board(air)

def draw_game():
    for rowcount,row in enumerate(game.gameboard):
        for columncount,block in enumerate(row):
            pygame.draw.rect(game.screen,block.color, pygame.Rect(rowcount *  PIXEL_WIDTH + MARGINX,columncount * PIXEL_HEIGHT + MARGINY, PIXEL_WIDTH, PIXEL_HEIGHT))

current_block = inventory[inventory_slot]
while game.get_running_state:
    main_clock.tick(FPS)
    game.screen.fill(gamemenager.White)
    draw_game()
    brush_size_text = gamemenager.font1.render(f"brush size :{brush_size}", True,gamemenager.red)
    current_block_text = gamemenager.font1.render(f"current block :{current_block.name}", True,gamemenager.red)
    game.screen.blit(brush_size_text,(0,0))
    game.screen.blit(current_block_text,(0,30))
    game.physicupdate()
    game.update_display()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            xpixel = (trunc((pos[0] - MARGINX) / PIXEL_WIDTH))
            ypixel = (trunc((pos[1] - MARGINY) / PIXEL_HEIGHT))
            # print(xpixel,ypixel)
            if brush_size == 1:
                game.gameboard[xpixel][ypixel] = current_block
            else:
                for x in range(brush_size):
                    for y in range(brush_size):
                        game.gameboard[xpixel][ypixel+y] = current_block
                        game.gameboard[xpixel+x][ypixel] = current_block
                        game.gameboard[xpixel-x][ypixel] = current_block
                        game.gameboard[xpixel][ypixel-y] = current_block
                        game.gameboard[xpixel-x][ypixel-y] = current_block
                        game.gameboard[xpixel+x][ypixel+y] = current_block
                        game.gameboard[xpixel-x][ypixel+y] = current_block
                        game.gameboard[xpixel+x][ypixel-y] = current_block



        if (event.type == pygame.KEYDOWN):
            if event.key == pygame.K_r:
                game.reset_board(air)
            if event.key == pygame.K_e:
                inventory_slot += 1
                if inventory_slot >= len(inventory):
                    inventory_slot = 0 
                current_block = inventory[inventory_slot]

        if event.type == pygame.MOUSEWHEEL:
            brush_size += event.y
            if brush_size < 1:
                brush_size = 1
            if brush_size > BRUSHSIZELIMIT:
                brush_size = BRUSHSIZELIMIT

            


