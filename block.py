from msilib.schema import Property
import pygame
import numpy as np

pygame.font.init()

class gamemenager:
    black = (0, 0, 0)
    yellow = (255, 255, 0)
    red = (255, 0, 0)
    White = (255, 255, 255)
    blue = (0, 0, 255)
    dark_gray = (80, 78, 81)
    green = (0, 255, 0)
    blue_sky = (135, 206, 235)
    brown = (165,42,42)
    stone_gray = (119,136,153)
    font1 = pygame.font.Font('freesansbold.ttf', 32)
    def __init__(self,name,screenwidth,screenheight,rendersizex,rendersizey) -> None:
        self.screen = None
        self.name = name
        self.screenwidth = screenwidth
        self.screenheight = screenheight
        self.running = True
        self.rendersizex = rendersizex
        self.rendersizey = rendersizey
        self.gameboard = []
        self.blocktype = ["solid","liquid","gas"]

    def set_up(self):
        self.screen = pygame.display.set_mode((self.screenwidth, self.screenheight))
        pygame.display.set_caption(self.name)

    def update_display(self):
        pygame.display.update()

    def create_board(self,defult_block):
        templist = []
        for row in range(self.rendersizex):
            for column in range(self.rendersizey):
                templist.append(defult_block)
            self.gameboard.append(templist)
            templist = []

    def reset_board(self,block):
        self.gameboard = []
        templist = []
        for row in range(self.rendersizex):
            for column in range(self.rendersizey):
                templist.append(block)
            self.gameboard.append(templist)
            templist = []

    def getting_around_block(self,block_location : tuple) -> dict:
        around = {"up" : self.gameboard[block_location[0]][block_location[1] - 1],
                  "right" : self.gameboard[block_location[0]+1][block_location[1]],
                  "left" : self.gameboard[block_location[0]-1][block_location[1]],
                  "down" : self.gameboard[block_location[0]][block_location[1] + 1],
                  "up_right" : self.gameboard[block_location[0] + 1][block_location[1] - 1],
                  "up_left" : self.gameboard[block_location[0] - 1][block_location[1] - 1],
                  "down_right" : self.gameboard[block_location[0] + 1][block_location[1] + 1],
                  "down_left" : self.gameboard[block_location[0] - 1][block_location[1] + 1],

                  "up_lo" : (block_location[0],block_location[1] - 1),
                  "right_lo" : (block_location[0]+1,block_location[1]),
                  "left_lo" : (block_location[0]-1,block_location[1]),
                  "down_lo" : (block_location[0],block_location[1] + 1),
                  "up_right_lo" : (block_location[0] + 1,block_location[1] - 1),
                  "up_left_lo" : (block_location[0] - 1,block_location[1] - 1),
                  "down_right_lo" : (block_location[0] + 1,block_location[1] + 1),
                  "down_left_lo" : (block_location[0] - 1,block_location[1] + 1)}
        return around

    def swap(self,block_location : tuple,block_swap_location : tuple):
        blocklocationx = block_location[0]
        blocklocationy = block_location[1]
        blockswaplocationx = block_swap_location[0]
        blockswaplocationy = block_swap_location[1]
        temp = self.gameboard[blockswaplocationx][blockswaplocationy]
        self.gameboard[blockswaplocationx][blockswaplocationy] = self.gameboard[blocklocationx][blocklocationy]
        self.gameboard[blocklocationx][blocklocationy] = temp
        
    def add_snapshot(self,block_location : tuple,block_swap : tuple):
        pass
                
    def physicupdate(self):
        snapshot = []
        for rownumber,row in enumerate(range(self.rendersizex)):
            for columnnumber,column in enumerate(range(self.rendersizey)):
                block : Block = self.gameboard[rownumber][columnnumber]
                if block.type == self.blocktype[0]:
                    pass
                # liquid physic
                elif block.type == self.blocktype[1]:
                    block_around = self.getting_around_block((rownumber,columnnumber))
                    if block_around["down"].type == self.blocktype[0]:
                        pass
                    elif (block_around["down"].type == self.blocktype[1]) and (block_around["down"].type != self.blocktype[2]):
                        if block.density >  block_around["down"].density:
                            # snapshot.append(((rownumber,columnnumber),("down_lo")))
                            self.swap((rownumber,columnnumber),block_around["down_lo"])
                        elif block.density == block_around["down"].density:
                            # if (((block_around["right"].density == block.density) and (block_around["left"].density == block.density))):
                            #     pass
                            # else:
                            if ((block.density > block_around["right"].density) and (block.density == block_around["left"].density)):
                                # snapshot.append(((rownumber,columnnumber),("right_lo")))
                                self.swap((rownumber,columnnumber),block_around["right_lo"])
                            elif ((block.density > block_around["left"].density) and (block.density == block_around["right"].density)):
                                # snapshot.append(((rownumber,columnnumber),("left_lo")))
                                self.swap((rownumber,columnnumber),block_around["left_lo"])

                    elif block_around["down"].type == self.blocktype[2]:
                        self.swap((rownumber,columnnumber),block_around["down_lo"])

        for i in snapshot:
            self.swap((i[0][0],i[0][1]),block_around[i[1]])
 

    @property
    def get_running_state(self):
        return self.running



class Block():
    #type = liquid solid gas
    def __init__(self,name,gamemenager,color,type,density) -> None:
        self.name = name
        self.gamemenager = gamemenager
        self.color = color
        self.type = type
        self.density = density
        
    # @abstractmethod
    # def update():
    #     pass

    @property
    def get_color(self):
        return self.color