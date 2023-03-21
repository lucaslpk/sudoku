import pygame
import time
from solver import solve, is_valid
pygame.font.init()          #pygame tutorial says we need to initialize the whole module i.e. pygame.init()

class Grid :

    def __init__(self, rows, cols, width, height):
        self.rows = rows            #this will always be 9 in a classic sudoku, but if we later want to do a 2x3 or 4x4 sudoku as an experiment
        self.cols = cols
        self.cubes = # this will be filled with a list comprehension creating a 9x9 matrix of 'cube' class objects
        self.width = width
        self.height = height
        #self.model = None
        self.selected = None

    def draw(self, screen):
        # Draw Grid Lines
        gap = self.width / 9
        for i in range(self.rows+1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(screen, (0,0,0), (0, i*gap), (self.width, i*gap), thick)
            pygame.draw.line(screen, (0,0,0), (i * gap, 0), (i * gap, self.height), thick)

    def select(self, row, col) :
        for i in range(self.rows) :                   # initially hardcoded as range(1,10) but later changed in accordance with tutorial's code, in case different size sudokus later
            for j in range(self.cols) :
                cubes[i][j].selected = False

        cubes[row][col].selected = True
        self.selected = (row, col)


def redraw_window(screen, board, play_time, strikes, font):
    screen.fill((255,255,255))                      
    text = font.render("Time: " + time_format(play_time), 1, (0,0,0))
    screen.blit(text, (380,560))
    if strikes == 1 :
        text = font.render(str(strikes) + " strike", 1, (255,0,0))
    else :
        text = font.render(str(strikes) + " strikes", 1, (255,0,0))
    screen.blit(text, (20,560))
    board.draw(screen)

def time_format(secs) :
    sec = secs % 60
    min = secs //60
    hrs = min // 60
    T_format = " " + str(min) + "m:" + str(sec) + "s"
    return T_format 

def main() :
    screen = pygame.display.set_mode((540,600))    #  Size is a tuple.
    pygame.display.set_caption("Sudoku")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 20) 
    board = Grid(9, 9, 540, 540)
    key = None
    run = True
    start = time.time()
    strikes = 0

    recColorRB = 0

    while run :
        clock.tick(255)
        play_time = round(time.time() - start)
        for event in pygame.event.get() :           # this loop will continously check of any event has happened and filter throughjt the list of defined events
            if event.type == pygame.QUIT :
                run = False
            if event.type == pygame.KEYDOWN :       # if event is a key press (or here keydown) check with the following which jey and what to do
                if event.key == pygame.K_1 :        # REFACTOR with case and with keys = pygame.key.get_pressed() z pierwszego video albo raczej jednokrotne nacisniecie bo pressed jest jak trzymiesz.
                    key = 1 
                if event.key == pygame.K_2 :        
                    key = 2
                if event.key == pygame.K_3 :        
                    key = 3
                if event.key == pygame.K_4 :        
                    key = 4
                if event.key == pygame.K_5 :        
                    key = 5
                if event.key == pygame.K_6 :        
                    key = 6
                if event.key == pygame.K_7 :        
                    key = 7
                if event.key == pygame.K_8 :        
                    key = 8
                if event.key == pygame.K_9 :        
                    key = 9
                if event.key == pygame.K_DELETE :        
                    #board.clear()                              # there will be a board object soon
                    key = None
                if event.key == pygame.K_RETURN :        
                    key = None                                                                                                                                                                                

            if event.type == pygame.MOUSEBUTTONDOWN :
                pos = pygame.mouse.get_pos()                    # returns a tuple of 2 ints
                clicked = board.click(pos)                      # feeds that tuple to click method of board instance
                if clicked :                                    # which returns True/False
                    board.select(clicked[0], clicked[1])        # calls select method with pos tuple values as arguments, this method sets board.selected to (row, col) tuple, set relevant cube.selected to True and all other cubes' "selected" to False
                    key = None                                  # resets key to empty but I don't yet know why

        if board.selected and key != None :                     # selected is a False or (row, col) tuple and a non-zero value  is True in python
            board.sketch(key)

        redraw_window(screen, board, play_time, strikes, font)
        # if recColorRB < 255 :
        #     pygame.draw.rect(screen, (recColorRB,255,recColorRB), (0,0, 540,600))
        #     recColorRB += 1
        pygame.display.update()

main()
pygame.quit()