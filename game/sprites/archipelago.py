from collections import deque

from scipy.stats import false_discovery_control

from game.sprites.island import *

class Archipelago:
    def __init__(self, height_matrix):
        self.board_surface = pygame.Surface((LEVEL_WIDTH, LEVEL_HEIGHT))
        self.heightMatrix = self.mapToString(height_matrix) # matrix of heights formed of input from Request.GET
        self.waterCells = [] # water cells array
        self.islands = [] # islands list
        self.idIslandSelected = -1
        self.idIsland = -1 # island array and island identificator used for dict. and array
        self.idHighestAvgIsland = -1 # island with highest avg height
        self.cellToIslandDict = { (-1,-1) : -1} # dictionary which links coordinates to island they belong to
        self.stillDrawings = [] # list used for storing drawings that are still
        self.movingDrawings = [] # list used for storing drawings that need to be updated
        self.populateMap() # filling out the map
        self.findHighestAvgIsland()


    def findHighestAvgIsland(self):
        if not self.islands:
            # there is not a single island
            self.idHighestAvgIsland = -1
            return
        self.idHighestAvgIsland = 0
        for i in range(len(self.islands)):
            if self.islands[self.idHighestAvgIsland].getAvgHeight() < self.islands[i].getAvgHeight():
                self.idHighestAvgIsland = i


    def mapToString(self, data_string):
        #accepts data matrix from URL provided, encapsulates it into useful matrix of heights
        matrix = []
        rows = data_string.strip().split('\n')
        for row in rows:
            matrix.append([int(x) for x in row.split()])
        return matrix


    def populateMap(self):
        self.populateTerrain()
        self.populateStillDrawings()


    def populateTerrain(self):
        for i in range(ROWS):
            for j in range(COLS):
                if self.heightMatrix[i][j] == 0:
                    self.makeWaterCell(i,j)
                else:
                    self.makeLandCell(i,j, self.heightMatrix[i][j])


    def makeWaterCell(self, i, j, height = 0):
        if height != 0:
            return
        cell = Terrain(i, j, height)
        self.waterCells.append(cell)


    def makeLandCell(self, i, j, height):
        if height <= 0:
            return
        self.assignLandToAnIsland(i, j)


    def assignLandToAnIsland(self, x, y):
        if x < 0 or x > COLS or y < 0 or y > ROWS:
            # invalid coordinates
            return -1
        if (x,y) in self.cellToIslandDict:
            # already is part of an island
            return self.cellToIslandDict[(x,y)]

        # new island
        newIsland = Island()
        self.idIsland += 1
        self.islands.append(newIsland)

        visited = [[False] * ROWS for _ in range(COLS)]
        queueBFS = deque()

        if not visited[x][y]:
            queueBFS.append((x,y))
            visited[x][y] = True

        while queueBFS:
            x,y = queueBFS.popleft()

            newIsland.addTerrainCell(Terrain(x, y, self.heightMatrix[x][y]), self.whereIsWaterSurrounding(x,y))
            self.cellToIslandDict[(x, y)] = self.idIsland
            for x_offs, y_offs in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                xx, yy = x + x_offs, y + y_offs
                if 0 <= xx < ROWS and 0 <= yy < COLS and self.heightMatrix[xx][yy] > 0 and not visited[xx][yy]:
                    queueBFS.append((xx, yy))
                    visited[xx][yy] = True
        return self.idIsland


    def whereIsWaterSurrounding(self,x, y):
        side = 0
        if x < 0 or x > COLS or y < 0 or y > ROWS:
            print("invalid coordinates for sides")
            return side
        for x_offset, y_offset in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            xx, yy = x + x_offset, y + y_offset
            if xx < 0 or xx >= ROWS or yy < 0 or yy >= COLS or self.heightMatrix[xx][yy] == 0:
                # if its next to the edge or next to water
                if x_offset == 0 and y_offset == 1:
                    side |= RedCellBorder.SIDE_DOWN
                if x_offset == 0 and y_offset == -1:
                    side |= RedCellBorder.SIDE_UP
                if x_offset == 1 and y_offset == 0:
                    side |= RedCellBorder.SIDE_RIGHT
                if x_offset == -1 and y_offset == 0:
                    side |= RedCellBorder.SIDE_LEFT
        return side


    def populateStillDrawings(self):
        self.populateShips()


    def populateShips(self): # populating our Archipelago with ships
        unsuccessCnt = 0
        for k in range(NUM_OF_SHIPS):
            while True:
                flag = False
                if(unsuccessCnt > k * 15): break
                x = random.randint(SHIP_WIDTH // TILESIZE + 1, ROWS - SHIP_WIDTH // TILESIZE - 1)
                y = random.randint(SHIP_HEIGHT // TILESIZE + 1, COLS - SHIP_HEIGHT // TILESIZE - 1)

                for i in range(x - SHIP_WIDTH // TILESIZE - 1, x + SHIP_WIDTH // TILESIZE+ 1):
                    for j in range(y - SHIP_HEIGHT // TILESIZE - 1, y + SHIP_HEIGHT // TILESIZE + 1):
                        if self.heightMatrix[i][j] != 0:
                            flag = True
                if flag:
                    unsuccessCnt += 1
                else:
                    ship = Ship(x, y)
                    for drawing in self.stillDrawings:
                        if drawing.overlaps(ship): flag = True

                    if not flag: self.stillDrawings.append(ship)
                    else: unsuccessCnt += 1

                    break


    def draw(self, screen): # draws whole Archipelago
        for waterCell in self.waterCells:
            waterCell.draw(self.board_surface)

        for island in self.islands:
            island.draw(self.board_surface)

        for still in self.stillDrawings:
            still.draw(self.board_surface)

        for moving in self.movingDrawings:
            moving.updateLocation()
            moving.draw(self.board_surface)
        screen.blit(self.board_surface, (0, 0))


    def selectIslandAt(self, x, y): # selects island at specific (x, y) coordinates

        if self.idIslandSelected != -1:
            # we look at any click as deselection of currently selected island
            self.islands[self.idIslandSelected].unselectIsland()
            self.idIslandSelected = -1

        if (x, y) not in self.cellToIslandDict:
            # if not clicked on island, return false
            #print("Missed island")
            return False

        self.idIslandSelected = self.cellToIslandDict[(x, y)]
        self.islands[self.idIslandSelected].selectIsland()
        #print("Clicked on island")

        if self.islands[self.idIslandSelected].getAvgHeight() == self.islands[self.idHighestAvgIsland].getAvgHeight():
            self.islands[self.idIslandSelected].showHeight(self.board_surface)
            #print("You selected highest!")
        return True

    def isHighestSelected(self):
        if self.idIslandSelected == -1:
            return False
        self.findHighestAvgIsland()
        if self.idIslandSelected != self.idHighestAvgIsland:
            return False
        return True

    def resetArchipelago(self):
        if self.idIslandSelected > -1:
            self.islands[self.idIslandSelected].unselectIsland()
        self.idIslandSelected = -1

    def display_board(self):
        for i in range(30):
            print("[", end=" ")
            for j in range(30):
                print(f"{self.heightMatrix[i][j]:4d}", end=", ")
            print("]", end=",")
            print("\n")