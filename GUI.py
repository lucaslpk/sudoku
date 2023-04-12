import pygame
import time
from solver import solve, is_valid, find_empty
from randPuzzle import puzzleAtLevel
from random import randint
pygame.font.init()          #pygame tutorial says we need to initialize the whole font module
gameSize = (9, 9)
screen = pygame.display.set_mode((540,750))    #  Size is a tuple.
clock = pygame.time.Clock()

class Grid :

    def __init__(self, board, rows, cols, width, height):
        self.board = board 
        self.rows = rows            #this will always be 9 in a classic sudoku, but if we later want to do a 2x3 or 4x4 sudoku as an experiment...
        self.cols = cols            # EDIT 11/04/23: now that an external board is passed to constructor as argument we could change to len(board) & len(board[0])
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(self.cols)] for i in range(self.rows)]  
        self.width = width
        self.height = height
        self.model = board           # model is a name of a temporary 9x9 board with cube value that needs to be checked. Model is passed to is_valid() and solve() to check if it's: 1) valid in terms of rows, columns and 3x3 squares 2) still leads to a valid solution
        self.selected = None        # this will hold a tuple with selected cube coordinates

    def draw(self, screen):
        # Draw Grid Lines
        gap = self.width / 9                    # hardcoded 9
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

    def click(self, pos) :                              # validates if click is within board and returns coordinates of relevant cube
        if pos[0] < self.width and pos[1] < self.height :
            gap = self.width / 9                        # again nine is hardcoded !!!! and gap is used for bothe width and height
            x = pos[0] // gap
            y = pos[1] // gap 
            print((x,y))
            return (int(y), int(x))                     # 1) y - vertical coordinate = row number, x horizontal coordinate = col number 2) x & y are results of an integer division ==> is int() conversion necessary here?
        else :
            return None    

    def place(self, val) :
        row, col = self.selected
        if self.cubes[row][col].value == 0 :            # you can only check if an empty cube is selected
            self.cubes[row][col].set(val)
            self.update_model()
            if is_valid(self.model, val, (row,col)) and solve(self.model) : # if both checks come back positive you got your number
                self.cubes[row][col].cubeColorRB = 0
                self.board[row][col] = self.cubes[row][col].value               # edit 12.04.23 - cube values were tracked in 'cube.value' property only, board.board WAS NOT updated as numbers where written in black (needed for autosolve animation as model is passed by ref)
                # print(is_valid(self.model, val, (row,col)), solve(self.model), 111) # this line and similar line in 'else' below ==> "print debugging" that helped me trouble shoot the issue with is_valid() method imported from solver file
                return True
            else :                                                          # or go back to board/model state before
                # print(is_valid(self.model, val, (row,col)), solve(self.model), 222)
                self.cubes[row][col].wrongNo = val
                self.cubes[row][col].wrongNoColorGB = 0                     # it makes more sense to trigger both color beaviours (green cube/red No) from inside "place" method than from RETURN key event in main loop
                self.cubes[row][col].set(0)                                 # because this is the namespace where val variable exists. You could trigger green cube form RETURN event in main loop (and I initially did) but not the red No. 
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False

    def sketch(self, val) :
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    def update_model(self) :
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]    

    def clear(self) :
        row, col = self.selected
        if self.cubes[row][col].value == 0 :     # you cannot clear a black number
            self.cubes[row][col].set_temp(0)

    def is_finished(self) :
        for i in range(self.rows) :
            for j in range(self.cols) :
                if self.cubes[i][j].value == 0 :
                    return False
        return True

class Cube :
    rows = gameSize[0]    # these don't seem to be used at all apart from here, would make snes if game had different sudoku sizes
    cols = gameSize[1]

    def __init__(self, value, row, col, width, height) : # width and height of the cube seem to be the same as Grid's W&H and later there is a gap var used which is width / hardcoded 9 ???
        self.value = value
        self.temp = []
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False
        self.cubeColorRB = 255
        self.wrongNo = None
        self.wrongNoColorGB = 255
        self.tempErrTimeOut = 0

    def set(self, val) :
        self.value = val

    def set_temp(self, val) :
        if val == 0 :                   # so taht we dont have te change every line where Cube set_temp method is called with arg = 0
            self.temp.clear()
        else :
            if val not in self.temp :
                self.temp.append(val)
            else :
                self.temp.pop(self.temp.index(val))

    def draw(self, screen) :
        gap = self.width / 9            # what I mentioned earlier - strange. the only reason I see would be consistency with Grid gap
        x = self.col * gap              
        y = self.row * gap
        line = ''  

        if len(self.temp) !=0 and self.value == 0 :                    # you can only sketch in a temp number in an empty cube Edit: legacy code "if self.temp !=0 and self.value == 0 "
            font = pygame.font.SysFont("comicsans", 16) 
            if self.tempErrTimeOut > 0 :
                text = font.render("Enter", 1 , (128,128,128))      
                screen.blit(text, (x+3, y+1))                            # hardcoded sizes and coordinates, works for fontsize 16, cube size 60x60, may not work for gam size 16x16
                text = font.render("Only", 1 , (128,128,128))      
                screen.blit(text, (x+3, y+19))
                text = font.render("One No", 1 , (128,128,128))      
                screen.blit(text, (x+3, y+37))
                self.tempErrTimeOut -= 5                          
                
            else :
                for i in range(int(gameSize[0]**0.5)) :                 # 0,1,2 for 9x9; 0,1,2,3 for 16x16 etc
                    for j in range(1, int(gameSize[0]**0.5) + 1) :      # 1,2,3 for 9x9; 1,2,3,4 for 16x16 etc
                        if int(i*gameSize[0]**0.5 + j) in self.temp :
                            line = str(int(i*gameSize[0]**0.5 + j)) 
                            text = font.render(line, 1 , (128,128,128))                                            
                            screen.blit(text, (x+6 + (j-1)*20, y+1 + i*(16+2)))                                    # hardcoded sizes, works for fontsize 16, cube size 60x60, may not work for 16x16
                
        elif self.value !=0 or self.wrongNo :                                     # and if value is set, it is set in stone and drawn in black, and if wrong - in slowly disappearing red
            font = pygame.font.SysFont("comicsans", 40) 
            if self.cubeColorRB < 255 :
                pygame.draw.rect(screen, (self.cubeColorRB,255,self.cubeColorRB), (x, y, gap, gap))
                self.cubeColorRB += 5
            if self.wrongNoColorGB < 255 :
                text = font.render(str(self.wrongNo), 1, (255,self.wrongNoColorGB,self.wrongNoColorGB))
                self.wrongNoColorGB += 5    
                if self.wrongNoColorGB == 255 :
                   self.wrongNo = None 
            else :                
                text = font.render(str(self.value), 1, (0,0,0))
            screen.blit(text, (x + gap/2 - text.get_width()/2, y + gap/2 - text.get_height()/2))

        if self.selected :
            pygame.draw.rect(screen, (255,0,0), (x, y, gap, gap), 3)

class Button : 
    font = pygame.font.SysFont("arial", 20)

    def __init__(self, text, x, y, w, h, enabled, screen):
        self.text = text
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.button_rect = pygame.rect.Rect(self.x, self.y, self.w, self.h)
        self.enabled = enabled
        self.draw(screen)

    def draw(self, screen) :
        button_text = self.font.render(self.text, True, ('black'))
        
        pygame.draw.rect(screen, 'gray', self.button_rect, 0, 5)            # solid grey
        pygame.draw.rect(screen, 'black', self.button_rect, 2, 5)           # edge in black
        screen.blit(button_text, (self.x + self.w//2 - button_text.get_width()//2, self.y + self.h//2 - button_text.get_height()//2))

    def check_click(self) :
        mouse_pos = pygame.mouse.get_pos()
        left_click = pygame.mouse.get_pressed()[0]  # get_pressed method returns all mouse button presses, [0] index is for left MB
        if left_click and self.button_rect.collidepoint(mouse_pos) and self.enabled :
            return True
        else:
            return False

def redraw_window(screen, board, play_time, strikes, font, buttons):
    screen.fill((255,255,255))                      
    text = font.render("Time: " + time_format(play_time), 1, (0,0,0))
    screen.blit(text, (380,560))
    if strikes == 1 :
        text = font.render(str(strikes) + " strike", 1, (255,0,0))
    else :
        text = font.render(str(strikes) + " strikes", 1, (255,0,0))
    screen.blit(text, (20,560))
    board.draw(screen)
    for button in buttons :
        button.draw(screen)

def time_format(secs) :
    sec = secs % 60
    min = secs //60
    hrs = min // 60
    T_format = " " + str(min) + "m:" + str(sec) + "s"
    return T_format 

def init() :
    pressed = False
    font1 = pygame.font.SysFont("arial", 40) 
    screen.fill((255,255,255)) 
    button_easy = Button("Easy", 20, 550, 110, 60, True, screen)
    button_normal = Button("Normal", 150, 550, 110, 60, True, screen)
    button_hard = Button("Hard", 280, 550, 110, 60, True, screen)
    button_expert = Button("Expert", 410, 550, 110, 60, True, screen)
    button_quit = Button("Quit", 410, 650, 110, 60, True, screen)
    buttons = [button_easy, button_normal, button_hard, button_expert, button_quit]

    while not pressed :
        clock.tick(10)
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                pygame.quit()
        if button_easy.check_click() :
            main(puzzleAtLevel(43))
        if button_normal.check_click() :
            main(puzzleAtLevel(50))
        if button_hard.check_click():
            main(puzzleAtLevel(54))    
        if button_expert.check_click():
            main(puzzleAtLevel(58))
        if button_quit.check_click() :
            pygame.quit()
        text = font1.render("Choose difficulty level:", 1, ("dark green"))
        screen.blit(text, (540//2 - text.get_width()//2, 440))
        for button in buttons :
            button.draw(screen)

        pygame.display.update()

def game_over():
    pressed = False
    font1 = pygame.font.SysFont("arial", 40) 
    button_replay = Button("Play Again", 20, 650, 110, 60, True, screen)
    button_newPuzzle = Button("New Puzzle", 150, 650, 110, 60, True, screen)
    button_home = Button("Home", 280, 650, 110, 60, True, screen)
    button_quit = Button("Quit", 410, 650, 110, 60, True, screen)
    buttons = [button_replay, button_newPuzzle, button_home, button_quit]

    while not pressed :
        clock.tick(10)
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                pygame.quit()
        if button_replay.check_click() :
            main()
        if button_newPuzzle.check_click() :
            pass
        if button_home.check_click():
            pass    
        if button_quit.check_click() :
            pygame.quit()
        text = font1.render("W E L L   D O N E", 1, ("dark green"))
        screen.blit(text, (540//2 - text.get_width()//2, 590))
        button_replay.draw(screen)
        button_quit.draw(screen)

        pygame.display.update()

def main(puzzle) :
    pygame.display.set_caption("Sudoku")
    font = pygame.font.SysFont("arial", 20) 
    board = Grid(puzzle,9, 9, 540, 540)
    button_restart = Button("Restart", 20, 650, 110, 60, True, screen)
    button_autosolve = Button("Solve", 150, 650, 110, 60, True, screen)
    button_home = Button("Home", 280, 650, 110, 60, True, screen)
    button_quit = Button("Quit", 410, 650, 110, 60, True, screen)
    buttons = [button_restart, button_autosolve, button_home, button_quit]
    key = None
    run = True
    autoSolving = False
    gameOverTimeOut = 0
    start = time.time()
    strikes = 0
    startloop = 0
    recColorRB = 0
    fpsAvg = []

    while run :
        clock.tick(255)
        play_time = round(time.time() - start)

        for event in pygame.event.get() :           # this loop will continously check of any event has happened and filter throughjt the list of defined events
            if autoSolving and not board.is_finished():
                pos = find_empty(board.board)
                if pos :
                    board.select(pos[0], pos[1])
                    key = randint(1,9)
                    board.sketch(key)
                    newevent = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN) #create the event
                    pygame.event.post(newevent)
                    key = None
                               
            if event.type == pygame.QUIT :
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN :       # if event is a key press (or here keydown) check with the following which jey and what to do
                if event.key in (pygame.K_1, pygame.K_KP1) :        # REFACTOR with case and with keys = pygame.key.get_pressed() z pierwszego video albo raczej jednokrotne nacisniecie bo pressed jest jak trzymiesz.
                    key = 1 
                if event.key in (pygame.K_2, pygame.K_KP2) :        
                    key = 2
                if event.key in (pygame.K_3, pygame.K_KP3) :        
                    key = 3
                if event.key in (pygame.K_4, pygame.K_KP4) :        
                    key = 4
                if event.key in (pygame.K_5, pygame.K_KP5) :        
                    key = 5
                if event.key in (pygame.K_6, pygame.K_KP6) :        
                    key = 6
                if event.key in (pygame.K_7, pygame.K_KP7) :        
                    key = 7
                if event.key in (pygame.K_8, pygame.K_KP8) :        
                    key = 8
                if event.key in (pygame.K_9, pygame.K_KP9):        
                    key = 9
                if event.key in (pygame.K_DELETE, pygame.K_BACKSPACE):        
                    board.clear()                             
                    key = None
                if event.key in (pygame.K_UP,pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT) :
                    if not board.selected:
                        board.select(0,0)
                    else :
                        row, col = board.selected
                        if event.key == pygame.K_UP :
                            if row == 0 :
                                board.select(board.rows - 1, col)
                            else:
                                board.select(row - 1, col)
                            key = None
                        if event.key == pygame.K_DOWN :
                            if row == board.rows - 1 :
                                board.select(0, col)
                            else:
                                board.select(row + 1, col)
                            key = None
                        if event.key == pygame.K_LEFT :
                            if col == 0 :
                                board.select(row, board.cols - 1)
                            else :
                                board.select(row, col - 1)
                            key = None
                        if event.key == pygame.K_RIGHT :
                            if col == board.cols - 1 :
                                board.select(row, 0)
                            else :
                                board.select(row, col + 1)
                            key = None
                if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER) :               # change temp to set
                    i, j = board.selected
                    if len(board.cubes[i][j].temp) == 0 :            # if there is a no temp value
                        pass
                    elif len(board.cubes[i][j].temp) == 1 :          # if there is exactly 1
                        result = board.place(board.cubes[i][j].temp[0]) # this runs the function and if it returns True or non-zero. Edit: result var is introduced so that we don't call the place() method each time we need to evaluate its result (twice)
                        if result :
                            print("Success")
                        elif result == None :                   # fix for "black-number-overwrite-attempt=strike" Bug
                            pass
                        else :
                            print("Wrong")
                            if not autoSolving :
                                strikes += 1
                    else :
                        board.cubes[i][j].tempErrTimeOut = 255
                    key = None                                                                                                                                                                                

                    if board.is_finished():
                        gameOverTimeOut = 255    

            if event.type == pygame.MOUSEBUTTONDOWN :
                if button_restart.check_click() :
                    main(puzzle)
                if button_autosolve.check_click() :
                    autoSolving = True
                    print("autosolving on")
                if button_home.check_click():
                    init()    
                if button_quit.check_click() :
                    pygame.quit()
                pos = pygame.mouse.get_pos()                    # returns a tuple of 2 ints
                clicked = board.click(pos)                      # feeds that tuple to click method of board instance
                if clicked :                                    # which returns True/False Edit: it actually returns a tuple (==> True) or None (==> False)
                    board.select(clicked[0], clicked[1])        # calls select method with pos tuple values as arguments, this method sets board.selected to (row, col) tuple, set relevant cube.selected to True and all other cubes' "selected" to False
                    key = None                                  # resets key to empty but I don't yet know why

        if board.selected and key != None :                     # selected is a False or (row, col) tuple and a non-zero value  is True in python
            board.sketch(key)
            key = None

        redraw_window(screen, board, play_time, strikes, font, buttons)

        if gameOverTimeOut > 0 :
            gameOverTimeOut -= 4                                # 12/04/23 if it only changes by -=1 it will hang on gOTO == zero
            print("gameOverTimeOut in '-=1 if'=", gameOverTimeOut) 
        elif gameOverTimeOut < 0 :
            print("gameOverTimeOut in 'else' =", gameOverTimeOut)
            game_over()

        # loop time measurement        
        if len(fpsAvg) < 100 :
            fpsAvg.append(round(1/(time.time() - startloop)))
        else :
            fpsAvg.pop(0)
            fpsAvg.append(round(1/(time.time() - startloop)))
        
        text = font.render(str(sum(fpsAvg)/len(fpsAvg)) + " fps", 1, (0,0,0))
        screen.blit(text, (100,560))
        startloop = time.time()
        # end time measurement
        pygame.display.update()
        
init()
#main()
pygame.quit()

# list of ideas:
# Added - autosolve button with animation --> 12/04/23 Not a very elegant solution but it only checks if board is finished after Enter key is pressed (legacy solution) instead every main loop run
# Added - multiple "penciled in" numbers
# Added - behaviour for success - fading out green Cube
# Added - behaviour for strike - red bold number fading out
# Note: there is a funny efect if you input correct solution after wrong one very quickly, but not sure if it's a bug or a feature
# Fixed - if you (even by mistake) try to overwrite a black number it counts as an error and adds 1 to strikes' count - that is a BUG. Edit: this happens because in this case board.place() method returns a default value (None) which is evaluated to False in RETURN key event
# Added - game over screen with quit and replay buttons
# Added - random solvable boards
# Added - difficulty levels with different amount of zeroes on board
# maybe different sizes - first research existing sudokus with 1-6 and 1-16 ranges
