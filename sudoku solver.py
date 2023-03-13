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
def print_board(bo) :
    print()
    for i in range(len(bo)) :
        if i % 3 == 0 and i !=0 :
            print("- - - - - - - - - - -")
        for j in range(len(bo[0])) :
            if j % 3 == 0 and j != 0 :
                print("|", end=" ")
            print(bo[i][j], end=" ")    
        print()
    print()   


def find_empty(bo) :
    for i in range(len(bo)) :
        for j in range(len(bo[0])) :
            if bo[i][j] == 0 :
                return i, j    #row column tuple

def is_valid(bo, num, pos) :
    
    for i in bo(pos[0]):          # this would work if we were inserting in this function. Since we will be inserting outside, pos tuple will hold the info where the number was inserted, and for that we need access to the index. So no enhanced for.
        if i == num :
            return False
        
    for j in range(len(bo)) :
        if bo([j][pos[1]]) == num :
            return False    

    bo[pos[0], pos[1]] == num

print_board(board)
print(find_empty(board))            