# Sample correct input:
sudo1 = """295743861
431865927
876192543
387459216
612387495
549216738
763524189
928671354
154938672"""

# Sample INcorrect input:

sudo2 = """195743862
431865927
876192543
387459216
612387495
549216738
763524189
928671354
254938671"""

sudo3 = """195743862
431865927
876192543
387459216
612387495
549216738
763524189
928671354
254938671"""

def convert(sudo) :
    splitlist = sudo.split("\n")
    if len(splitlist) != 9 :
        print("Something wrong with how data is formated or you don't have 9 rows.")
        exit()
    
    m9x9 = [""for i in range(9)]
    for i in range(9):
        if len(splitlist[i]) != 9 :
            print("One of the rows doesn't have 9 numbers or has extra spaces.")
            exit()
        m9x9[i] = list(splitlist[i])
    return m9x9

def rowCheck(table) :
    for i in range(9) :
        row = ''.join(table[i])
        for j in range(1, 10) :
            if row.count(str(j)) != 1 :
                print("Row No ", i, "is invalid.")
                return
    print("All rows valid.")    

def colCheck(table):   
    for j in range(9) : 
        col = []
        for i in range(9) :
            col.append(table[i][j]) 
        col =''.join(col)
        
        for k in range(1, 10) :
            if col.count(str(k)) != 1 :
                print("Col No ", i, "is invalid.")  
                return
    print("All columns valid.")            

def squareCheck(table) :
    anySqInvalid = False
    for x in range(0, 7, 3):
        for y in range(0, 7, 3):
            sq = []
            for j in range(x, 3 + x) : 
                for i in range(y, 3 + y) :
                    sq.append(table[i][j]) 
            sq =''.join(sq)
            
            for k in range(1, 10) :
                    if sq.count(str(k)) > 1 :
                        anySqInvalid = True
                        print("Square starting @(", x,",", y,") is invalid.", sep="")
    if not anySqInvalid :                         
        print("All squares valid.")

def tripleCheck(table) :
    rowCheck(convert(table))
    colCheck(convert(table))
    squareCheck(convert(table))

def main() :
    tripleCheck(sudo3)

main()