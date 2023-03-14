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
            
    return False        # if no empties return False

def is_valid(bo, num, pos) :
    for i in bo[pos[0]]:         #returned to 'enhanced for' as per my initial "gut feeling"
        if i == num :
            return False
        
    for j in range(len(bo)) :
        if bo[j][pos[1]] == num :
            return False    

    for i in range(pos[0] // 3 * 3, pos[0] // 3 * 3 + 3) :
        for j in range(pos[1] // 3 * 3, pos[1] // 3 * 3 + 3) :
            if bo[i][j] == num :
                return False

    return True

def solve(bo) :
    find = find_empty(bo)        # var name == "a find" (noun) == means a find returned by by the function, a find == tuple or False
    if not find :                # non-zero value is interpreted as True in Python
        return True
    
    for x in range(1, 10) :
        if is_valid(bo, x, find) :
            bo[find[0]][find[1]] = x

            if solve(bo) :
                return True

            bo[find[0]][find[1]] = 0

    return False        

print_board(board)
solve(board)            
print_board(board)              # it will print the solved board, because lists are objects and therefore it was passed by reference.