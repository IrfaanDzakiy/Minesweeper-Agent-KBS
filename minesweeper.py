import numpy


class cell:
    def __init__(self, x, y, visible):
        # 0 hidden
        # 1 show
        # 2 flagged
        self.visibile = visible
        self.x = x
        self.y = y
        
    def setVisiblility(self, visible):
        self.visibile = visible


class board:
    def __init__(self, n):
        self.n = n
        # * hidden
        # # show
        self.board = [['*' for i in range(n)] for j in range(n)] 
        self.mines = [[False for i in range(n)] for j in range(n)]
        self.number = [[0 for i in range(n)] for j in range(n)]
        self.win = None
        self.totalMines= 0
        self.noMines = 0
        
    def placeMines(self, totalMines):
        for i in range(totalMines):
            self.noMines = pow(self.n, 2) - totalMines
            loc = input()
            x, y = loc.split(",")
            self.mines[int(x)][int(y)] = True
            self.number[int(x)][int(y)] = 99
            
    def placeMinesByFile(self, files):
        file = open(files)
        self.totalMines = int(file.readline())
        self.noMines = pow(self.n, 2) - self.totalMines
        for i in range(self.totalMines):
            loc = file.readline()
            x, y = loc.split(",")
            self.mines[int(x)][int(y)] = True
            self.number[int(x)][int(y)] = 99
        print("Total Cell with no mines = ", board.noMines)
        print("Total Cell with mines = ", board.totalMines)
        
            
    def createNumber(self):
        for i in range(self.n):
            for j in range(self.n):
                if self.mines[i][j] == True:
                    for a in range(-1, 2):
                        for b in range(-1, 2):
                            if not (a==0 and b==0):
                                if i+a >= 0 and j+b >= 0 and i+a <= self.n-1 and j+b <= self.n-1 :
                                    if self.mines[i+a][j+b] != True:
                                        self.number[i+a][j+b] += 1
    
    def printBoard(self):
        for i in range(self.n):
            for j in range(self.n):
                print(self.board[i][j], end=" ")
            print()
            
    def printMinesBoard(self):
        for i in range(self.n):
            for j in range(self.n):
                print(self.mines[i][j], end=" ")
            print()
                                
        else:
            self.win = False                       
            return 
        
    
    def isWin(self):
        if self.win != None:
            if self.win == True:
                print("Congratulataion!!")
            else:
                print("You Lose!!")
            

    # * hidden # show
    # self.board = [['*' for i in range(n)] for j in range(n)] 
    # self.mines = [[False for i in range(n)] for j in range(n)]
    # self.number = [[0 for i in range(n)] for j in range(n)]
    def penpen(self, x, y):
        if self.board[x][y] == '*':
            self.board[x][y] = '#'
            # print("replaced ", x, ", ", y)
            self.noMines -= 1
        if self.number[x][y] == 0:
            if (y >=0 and y <= self.n-2) and (x >= 0 and x <= self.n-1):
                if self.board[x][y+1] == '*':
                    self.penpen(x,y+1)
            if (y >=1 and y <= self.n-1) and (x >= 0 and x <= self.n-1):
                if self.board[x][y-1] == '*':
                    self.penpen(x,y-1)
            if (y >= 1 and y <= self.n-1) and (x >= 1 and x <= self.n-1):
                if self.board[x-1][y-1] == '*':
                    self.penpen(x-1,y-1)
            if (y >= 0 and y <= self.n-2) and (x >= 1 and x <= self.n-1):
                if self.board[x-1][y+1] == '*':
                    self.penpen(x-1,y+1) 
            if (y >= 0 and y <= self.n-1) and (x >= 1 and x <= self.n-1):
                if self.board[x-1][y] == '*':
                    self.penpen(x-1,y)
            if (y >=0 and y <= self.n-2) and (x >= 0 and x <= self.n-2):
                if self.board[x+1][y+1] == '*':
                    self.penpen(x+1,y+1)
            if (y >= 1 and y <= self.n-1) and (x >= 0 and x <= self.n-2):
                if self.board[x+1][y-1] == '*':
                    self.penpen(x+1,y-1)
            if (y >= 0 and y <= self.n-1) and (x >= 0 and x <= self.n-2):
                if self.board[x+1][y] == '*':
                    self.penpen(x+1,y)
    
    
    def checkWinner(self):
        if self.win == None:
            if self.noMines == 0:
                self.win == True
        
        if self.win == True:
            print("Congratulataion!!")
            
        elif self.win == False:
            print("You Lose!!")
    
            
    def open(self, x, y):
        # not bomb
        # if self.mines[x][y] != True:
        #     if self.number[x][y] > 0: 
        #         self.board[x][y] = '#'
        #     else:
        #         self.board[x][y] = '#'
        #         for a in range(-1, 2):
        #             for b in range(-1,2):
        #                 if x+a >= 0 and y+b >= 0 and x+a <= self.n-1 and y+b <= self.n-1 :
        #                     self.open(x+a, y+b)
        #                     return
                                
        #         # return
                
        self.board[x][y] = '*'
        if self.number[x][y] == 0:
            for a in range(-1, 2):
                for b in range(-1,2):
                    if not (a==0 and b==0):
                        if x+a >= 0 and y+b >= 0 and x+a <= self.n-1 and y+b <= self.n-1 :
                            if self.board[x+a][y+b] == '*':
                                # self.open(x+a,y+b)
                                self.penpen(x+a,y+b)
        else:
            return    
        

    
    
            
board = board(10)
# board.placeMines(4)
board.placeMinesByFile("input.txt")
board.createNumber()
# board.printBoard()
# board.printMinesBoard()
# print(numpy.array(board.board))
print(numpy.array(board.mines))
print(numpy.array(board.number))
# print(type( 1))
# # print(type(int(" 1")))

while board.checkWinner()==None:
    inp = input("Masukkan nilai x dan y dengan format x, y = ")
    x, y = inp.split(",")
    # board.open(int(x), int(y))
    board.penpen(int(x), int(y))
    board.printBoard()
    print("Total Cell with no mines = ", board.noMines)
    print("Total Cell with mines = ", board.totalMines)
    
    # board.checkWinner()
    if board.checkWinner() != None:
        break