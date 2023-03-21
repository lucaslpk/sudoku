import pygame
import time
from solver import solve, is_valid
pygame.font.init()          #pygame tutorial says we need to initialize the whole module i.e. pygame.init()
gameSize = (9, 9)

class Grid :
    board = [
    [0,0,2,0,8,0,0,6,0],
    [0,5,6,9,1,7,0,3,0],
    [0,4,0,0,5,0,8,7,1],
    [0,9,0,0,0,0,6,0,0],
    [6,7,1,0,9,5,2,0,0],
    [0,0,0,0,2,0,1,0,0],
    [1,6,7,0,3,0,5,9,0],
    [4,8,0,0,7,0,3,0,0],
    [0,2,5,4,6,0,0,0,0]
    ]

    def __init__(self, rows, cols, width, height):
        self.rows = rows            #this will always be 9 in a classic sudoku, but if we later want to do a 2x3 or 4x4 sudoku as an experiment
        self.cols = cols
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for i in range(self.rows)] for j in range(self.cols)]   # tutorial code has ...)for j ] for i ] other way around - I wonder if it matters?
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

        for i in range(self.rows) :
            for j in range(self.cols) :
                self.cubes[i][j].draw(screen)

    def select(self, row, col) :
        for i in range(self.rows) :                   # initially hardcoded as range(1,10) but later changed in accordance with tutorial's code, in case different size sudokus later
            for j in range(self.cols) :
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def click(self, pos) :                              # validates if click is within board and returns (x,y) of a top left corner of relevant cube
        if pos[0] < self.width and pos[1] < self.height :
            gap = self.width / 9                        # again nine is hardcoded !!!! and gap is used for bothe width and height
            x = pos[0] // gap
            y = pos[1] // gap 
            print((x,y))
            return (int(x), int(y))                     # x & y are result of an integer division ==> is int() conversion necessary here?
        else :
            return None    


class Cube :
    rows = gameSize[0]    # these don't seem to be used at all 
    cols = gameSize[1]

    def __init__(self, value, row, col, width, height) : # width and height of the cube seem to be the same as Grid's W&H and later there is a gap var used which is width / hardcoded 9 ???
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def set(self, val) :
        self.value = val

    def set_temp(self, val) :
        self.temp = val

    def draw(self, screen) :
        font = pygame.font.SysFont("comicsans", 40) 

        gap = self.width / 9            # what I mentioned earlier - strange. the only reason I see would be consistency with Grid gap
        x = self.col * gap              
        y = self.row * gap

        if self.temp !=0 and self.value == 0 :                    # you can only sketch in a temp number in an empty cube
            text = font.render(str(self.temp), 1, (128,128,128))
            screen.blit(text, (x+5, y+5))
        elif self.value !=0 :                                     # and if value is set, it is set in stone and drawn in black
            text = font.render(str(self.value), 1, (0,0,0))
            screen.blit(text, (x + gap/2 - text.get_width()/2, y + gap/2 - text.get_height()/2))

        if self.selected :
            pygame.draw.rect(screen, (255,0,0), (x, y, gap, gap), 3)
            
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
                if clicked :                                    # which returns True/False Edit: it actually return a tuple (==> True) or None (==> False)
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