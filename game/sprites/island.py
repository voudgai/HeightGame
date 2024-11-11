from .drawings import *

class Island:
    def __init__(self):
        self.terrainCells = []
        self.redLines = []
        self.blackLines = []

        self.selected = False
        self.totalHeight = 0
        self.numberOfCells = 0
        # this cell is not inside terrain cells, used just for comparison to get the highest
        self.highestCell = Terrain(0,0,0)
        self.heightImage = empty_image


    def addTerrainCell(self, terrainCell, waterSides):
        self.terrainCells.append(terrainCell)
        self.redLines.append(RedCellBorder(terrainCell.x, terrainCell.y, waterSides))
        self.blackLines.append(BlackCellBorder(terrainCell.x, terrainCell.y, waterSides))
        self.numberOfCells += 1
        self.totalHeight += terrainCell.height
        if self.highestCell.height < terrainCell.height:
            self.highestCell = terrainCell


    def draw(self, board_surface):
        for terrainCell in self.terrainCells:
            terrainCell.draw(board_surface)
        if self.selected:
            for redLine in self.redLines:
                redLine.draw(board_surface)
        else:
            for blackLine in self.blackLines:
                blackLine.draw(board_surface)
        if self.heightImage != empty_image and self.selected:
            x = self.highestCell.x
            y = self.highestCell.y
            board_surface.blit(self.heightImage, (x, y))


    def selectIsland(self):
        print("Selected island\n")
        self.selected = True


    def unselectIsland(self):
        print("Unselected island\n")
        self.selected = False


    def getAvgHeight(self):
        return self.totalHeight // self.numberOfCells


    def showHeight(self, board_surface):
        self.heightImage = getHeightSignImage(self.getAvgHeight())

    def hideHeight(self):
        self.heightImage = empty_image