
import MyExceptions

class Game:

    def __init__(self):
        
        self.grid = []
        self.tempGrid = []
        self.gridSize = 3 # default to 3 if 0 initial cells entered
        self.newCellCoordsList = []
        self.extendGridIn = False # flag for live cell on inner side of grid (ie x=0 or y=0)
        self.extendGridOut = False # flag for live cell on outer side of grid

    def populateInitialGrid(self):
        while True:
            try:
                initialCellCount = int(input("Enter number of inital live cells: "))
                if initialCellCount<0:
                    raise MyExceptions.NegativeLiveCellsError
                break
            except ValueError:
                print("Not a valid number of cells. Please start again")
            except MyExceptions.NegativeLiveCellsError:
                print("Please enter a positive number of initial live cells")

        for i in range(initialCellCount):
            while True:
                try:
                    x,y = input("Please enter x and y coordinates for intial live cell {} seperated by a space: ".format(i+1)).split()
                    x = int(x)
                    y = int(y)
                    if [x,y] in self.newCellCoordsList:
                        raise MyExceptions.IdenticalCoordinatesError
                    elif x<0 or y<0:
                        raise MyExceptions.NegativeCoordinateError
                    else:
                        self.newCellCoordsList.append([x,y])
                    break
                except ValueError:
                    print("You have not entered 2 valid coordinates. Please try again")
                except MyExceptions.IdenticalCoordinatesError:
                    print("You have already entered these coordinates. Please try again")
                except MyExceptions.NegativeCoordinateError:
                    print("Please only enter positive coordinates")

        if initialCellCount != 0:
            self.gridSize = (max(max(self.newCellCoordsList, key=max))) + 2  #finding max single coordinate value from list of lists
    
        self.grid = self.buildEmptyGrid(self.gridSize)

        for aliveCell in self.newCellCoordsList:
            self.grid[aliveCell[1]][aliveCell[0]] = True
            if aliveCell[0] == 0 or aliveCell[1] == 0:  # need to check initial cells on inner border, adding 2 to self.gridSize removes need for outside border check
                self.extendGridIn = True
        self.extendBorders()
           
    def printGrid(self):
        for x in range(len(self.grid[0])):
            for y in range(len(self.grid)):
                if self.grid[x][y] == True:
                    print("*", end = " ")
                else:
                    print("-", end = " ")
            print()
        print()

    def buildEmptyGrid(self, gridSize):
        grid = [[False for _ in range(gridSize)]for _ in range(gridSize)]
        return grid

    def evolution(self):
        self.tempGrid = self.buildEmptyGrid(self.gridSize) #need 2 grids as cant modify 1 before evaluating each live cell

        for x in range(len(self.grid[0])):
            for y in range(len(self.grid)):
                self.findNeighbours(x, y)   # check neighbours for every dead or alive cell on the grid

        self.grid = self.tempGrid # replace with updates grid

    def findNeighbours(self, x, y):

        nCount = 0
       
        try:
            for i in range(-1,2):
                for j in range(-1,2):
                    if self.grid[x+i][y+j] and not (x+i==x and y+j==y):
                        nCount += 1
        except IndexError:
            pass
        
       
        if nCount < 2:
            self.tempGrid[x][y] = False
        elif nCount > 3:
            self.tempGrid[x][y] = False
        elif nCount == 2 and self.grid[x][y]:
            self.tempGrid[x][y] = True
        elif nCount == 3 and not self.grid[x][y]:
            self.tempGrid[x][y] = True

        if self.tempGrid[x][y]:
            if x==0 or y==0:
                self.extendGridIn = True
            if x==(self.gridSize-1) or y==(self.gridSize-1):
                self.extendGridOut = True
    
    def extendBorders(self):
        
        newRow = [False for _ in range((self.gridSize+1))]

        if self.extendGridIn:
            for row in range(len(self.grid)):
                self.grid[row].insert(0, False)

            self.grid.insert(0, newRow)
            self.extendGridIn = False
            self.gridSize += 1  #gridSize is used in multiple functions so needs to be updated
        
        if self.extendGridOut:
            for row in range(len(self.grid)):
                self.grid[row].append(False)

            self.grid.append(newRow)
            self.extendGridOut = False
            self.gridSize += 1 
            
    def startGame(self):
        self.populateInitialGrid()
        self.printGrid()
        
        while True:
            action = input("Please enter 's' to stop the program or anything else to continue onto the next iteration: ")
            if action == "s":
                break
            self.evolution()
            if self.extendGridIn or self.extendGridOut:
                self.extendBorders()
            self.printGrid()
            
        
g = Game()
g.startGame()


"""
Assumptions made:
    - As the problem states 'infinite 2d space', thhere are no 'set' borders to the game space and the gridSize of the grid should grow as neccessary.

"""