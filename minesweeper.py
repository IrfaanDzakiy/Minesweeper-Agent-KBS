import numpy


class cell:
    def __init__(self):
        # 0 hidden
        # 1 show
        # 2 flagged
        self.visibile = 0
        self.mine = False
        self.number = 0
        self.x = 0
        self.y = 0
    
    def setX(self, x):
        self.x = x
        
    def setY(self, y):
        self.y = y
        
    def setVisiblility(self, visible):
        self.visibile = visible

    def setMine(self, mine):
        self.mine = mine
        
    def setNumber(self, number):
        self.number = number

class board:
    def __init__(self, n):
        self.n = n
        # * hidden
        # # show
        self.win = None
        self.totalMines= 0
        self.noMines = 0
        self.board = [[cell() for i in range(n)] for j in range(n)]
        self.flag = 0
        
    def placeMines(self, totalMines):
        self.totalMines = totalMines
        self.flag = self.totalMines
        for i in range(totalMines):
            self.noMines = pow(self.n, 2) - totalMines
            loc = input()
            x, y = loc.split(",")
            self.board[int(x)][int(y)].setX(int(x))
            self.board[int(x)][int(y)].setY(int(y))
            self.board[int(x)][int(y)].setMine(True)
            self.board[int(x)][int(y)].setNumber('X')
            
    def placeMinesByFile(self, files):
        file = open(files)
        self.totalMines = int(file.readline())
        self.flag = self.totalMines
        self.noMines = pow(self.n, 2) - self.totalMines
        for i in range(self.totalMines):
            loc = file.readline()
            x, y = loc.split(",")
            self.board[int(x)][int(y)].setX(int(x))
            self.board[int(x)][int(y)].setY(int(y))
            self.board[int(x)][int(y)].setMine(True)
            self.board[int(x)][int(y)].setNumber('X')
        print("Total Cell with no mines = ", board.noMines)
        print("Total Cell with mines = ", board.totalMines)
        
            
    def createNumber(self):
        for i in range(self.n):
            for j in range(self.n):
                if self.board[i][j].mine == True:
                    for a in range(-1, 2):
                        for b in range(-1, 2):
                            if not (a==0 and b==0):
                                if i+a >= 0 and j+b >= 0 and i+a <= self.n-1 and j+b <= self.n-1 :
                                    if self.board[i+a][j+b].mine != True:
                                        self.board[i+a][j+b].number += 1
    
    def printBoard(self):
        print("masook")
        for i in range(self.n):
            for j in range(self.n):
                if self.board[i][j].visibile == 0:
                    print("*", end=" ")
                elif self.board[i][j].visibile == 1:
                    if self.board[i][j].number != 0:
                        print(self.board[i][j].number, end=" ")
                    else:
                        print("#", end=" ")
                else:
                    print("F", end=" ")
            print()
            
    
    def isWin(self):
        if self.win != None:
            if self.win == True:
                print("Congratulataion!!")
            else:
                print("You Lose!!")
            

    def setFlag(self, x, y):
        if self.flag >= 0:
            self.board[x][y].setVisiblility(2)
    
    def unsetFlag(self, x, y):
        if self.flag >= 0:
            self.board[x][y].setVisiblility(0)


    # * hidden 
    # # show
    def open(self, x, y):
        if self.board[x][y].visibile == 0:
            self.board[x][y].visibile = 1
            # print("replaced ", x, ", ", y)
            self.noMines -= 1
        if self.board[x][y].number == 0:
            if (y >=0 and y <= self.n-2) and (x >= 0 and x <= self.n-1):
                if self.board[x][y+1].visibile == 0:
                    self.open(x,y+1)
            if (y >=1 and y <= self.n-1) and (x >= 0 and x <= self.n-1):
                if self.board[x][y-1].visibile == 0:
                    self.open(x,y-1)
            if (y >= 1 and y <= self.n-1) and (x >= 1 and x <= self.n-1):
                if self.board[x-1][y-1].visibile == 0:
                    self.open(x-1,y-1)
            if (y >= 0 and y <= self.n-2) and (x >= 1 and x <= self.n-1):
                if self.board[x-1][y+1].visibile == 0:
                    self.open(x-1,y+1) 
            if (y >= 0 and y <= self.n-1) and (x >= 1 and x <= self.n-1):
                if self.board[x-1][y].visibile == 0:
                    self.open(x-1,y)
            if (y >=0 and y <= self.n-2) and (x >= 0 and x <= self.n-2):
                if self.board[x+1][y+1].visibile == 0:
                    self.open(x+1,y+1)
            if (y >= 1 and y <= self.n-1) and (x >= 0 and x <= self.n-2):
                if self.board[x+1][y-1].visibile == 0:
                    self.open(x+1,y-1)
            if (y >= 0 and y <= self.n-1) and (x >= 0 and x <= self.n-2):
                if self.board[x+1][y].visibile == 0:
                    self.open(x+1,y)
    
    
    def checkWinner(self):
        
        if self.noMines == 0:
            self.win = True
        
        if self.win == True:
            print("Congratulataion!!")
            
        elif self.win == False:
            print("You Lose!!")
    
            
    
        

    
    
            
board = board(10)
board.placeMinesByFile("input.txt")
board.createNumber()
board.printBoard()

while board.win==None:
    inp = input("Masukkan nilai x dan y dengan format x, y = ")
    x, y = inp.split(",")
    board.open(int(x), int(y))
    board.printBoard()
    print("Total Cell with no mines = ", board.noMines)
    print("Total Cell with mines = ", board.totalMines)
    
    board.checkWinner()