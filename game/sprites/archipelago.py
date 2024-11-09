from .island import *

class Archipelago:
    def __init__(self, height_matrix):
        self.board_surface = pygame.Surface((WIDTH, HEIGHT))
        self.heightMatrix = self.mapToString(height_matrix) # matrix of heights formed of input from Request.GET
        self.terrainMatrix = [[]] # matrix of terrain cells formed with heights matrix
        self.waterCells = [] # water cells array
        self.islands = []
        self.idIsland = -1 # island array and island identificator used for dict. and array
        self.cellToIslandDict = {} # dictionary which links coordinates to island they belong to
        self.stillDrawings = [] # list used for storing drawings that are still
        self.movingDrawings = [] # list used for storing drawings that need to be updated
        self.populateMap() # filling out the map

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
        terrainRow = []
        for i in range(ROWS):
            for j in range(COLS):
                self.makeTerrainCell(i, j, self.heightMatrix[i][j], terrainRow)
            self.terrainMatrix.append(terrainRow)
            terrainRow = []

    def makeTerrainCell(self, i, j, height, terrainRow):
        cell = Terrain(i, j, height)
        terrainRow.append(cell)
        if self.heightMatrix[i][j] > 0: # if its land cell
            cellIslandID = self.getIslandForCell(i, j)
            if cellIslandID != -1:
                self.islands[cellIslandID].addTerrainCell(cell, self.whereIsWater(i, j))
        else: # its water cell
            self.waterCells.append(cell)

    def whereIsWater(self,x, y):
        side = 0
        if x < 0 or x > COLS or y < 0 or y > ROWS:
            print("invalid coordinates for sides")
            return side
        for x_offset, y_offset in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            if 0 <= x + x_offset <= COLS - 1 and 0 <= y + y_offset <= ROWS - 1 and self.heightMatrix[x + x_offset][y + y_offset] == 0:
                if x_offset == 0 and y_offset == 1:
                    side |= RedCellBorder.SIDE_DOWN
                if x_offset == 0 and y_offset == -1:
                    side |= RedCellBorder.SIDE_UP
                if x_offset == 1 and y_offset == 0:
                    side |= RedCellBorder.SIDE_RIGHT
                if x_offset == -1 and y_offset == 0:
                    side |= RedCellBorder.SIDE_LEFT
        return side

    def getIslandForCell(self, x, y):
        if x < 0 or x > COLS or y < 0 or y > ROWS:
            print("invalid coordinates for sides")
            return -1

        for x_offset, y_offset in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            if 0 <= x + x_offset <= COLS - 1 and 0 <= y + y_offset <= ROWS - 1 and  (x + x_offset, y + y_offset) in self.cellToIslandDict:
                return self.cellToIslandDict[(x + x_offset, y + y_offset)]
        # first time this island occurs
        self.idIsland += 1
        self.islands.append(Island())
        return self.idIsland

    def populateStillDrawings(self):
        self.populateShips()

    def populateShips(self):
        unsuccessCnt = 0
        for k in range(NUM_OF_SHIPS):
            while True:
                if(unsuccessCnt > k * 15): break
                x = random.randint(SHIP_WIDTH // TILESIZE + 1, ROWS - SHIP_WIDTH // TILESIZE - 1)
                y = random.randint(SHIP_HEIGHT // TILESIZE + 1, COLS - SHIP_HEIGHT // TILESIZE - 1)
                flag = False
                for i in range(x - SHIP_WIDTH // TILESIZE - 1, x + SHIP_WIDTH // TILESIZE+ 1):
                    for j in range(y - SHIP_HEIGHT // TILESIZE - 1, y + SHIP_HEIGHT // TILESIZE + 1):
                        if self.heightMatrix[i][j] != 0:
                            flag = True
                if flag:
                    unsuccessCnt += 1
                    continue
                self.stillDrawings.append(Ship(x, y))
                break

    def draw(self, screen):
        for island in self.islands:
            island.draw(self.board_surface)

        for waterCell in self.waterCells:
            waterCell.draw(self.board_surface)

        for still in self.stillDrawings:
            still.draw(self.board_surface)

        for moving in self.movingDrawings:
            moving.updateLocation()
            moving.draw(self.board_surface)
        screen.blit(self.board_surface, (0, 0))

    def display_board(self):
        for i in range(30):
            print("[", end=" ")
            for j in range(30):
                print(f"{self.heightMatrix[i][j]:4d}", end=", ")
            print("]", end=",")
            print("\n")