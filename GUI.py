import pygame
import time
from solver import solve, is_valid
pygame.font.init()          #pygame tutorial says we need to initialize the whole module i.e. pygame.init()

class Grid :

    def __init__(self, rows, cols, width, height):
        self.rows = rows
        self.cols = cols
        #self.cubes =
        self.width = width
        self.height = height
        #self.model = None
        #self.selected = None

    def draw(self, win):
        # Draw Grid Lines
        gap = self.width / 9
        for i in range(self.rows+1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(win, (0,0,0), (0, i*gap), (self.width, i*gap), thick)
            pygame.draw.line(win, (0,0,0), (i * gap, 0), (i * gap, self.height), thick)


def redraw_window(win, board, time, strikes):
    win.fill((255,255,255))
    font = pygame.font.SysFont("arial", 20)
    text = font.render("Time: " + str(time), 1, (0,0,0))
    win.blit(text, (380,560))
    if strikes == 1 :
        text = font.render(str(strikes) + " strike", 1, (255,0,0))
    if strikes != 1 :
        text = font.render(str(strikes) + " strikes", 1, (255,0,0))
    win.blit(text, (20,560))

def main() :
    win = pygame.display.set_mode((540,600))    # win is for window and NOT for a win/lose boolean as I initially thought. Size is a tuple.
    pygame.display.set_caption("Sudoku")
    board = Grid(9, 9, 540, 540)
    key = None
    run = True
    start = time.time()
    strikes = 0

    while run :
        play_time = round(time.time() - start)
        for event in pygame.event.get() :           # this loop will continously check of any event has happened and filter throughjt the list of defined events
            if event.type == pygame.QUIT :
                run = False
            if event.type == pygame.KEYDOWN :       # if event is a key press (or here keydown) check with the following which jey and what to do
                if event.key == pygame.K_1 :        # REFACTOR with case
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
                    #board.clear()                    # there will be a board class object soon
                    key = None
                if event.key == pygame.K_RETURN :        
                    key = None                                                                                                                                                                                


        redraw_window(win, board, play_time, strikes)
        pygame.display.update()

main()
pygame.quit()