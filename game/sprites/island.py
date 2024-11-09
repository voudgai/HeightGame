from .drawings import *

class Island:
    def __init__(self):
        self.terrainCells = []
        self.redLines = []

        self.selected = False
        self.totalHeight = 0
        self.numberOfCells = 0

    def addTerrainCell(self, terrainCell, redLineSide):
        self.terrainCells.append(terrainCell)
        self.redLines.append(RedCellBorder(terrainCell.x, terrainCell.y, redLineSide))
        self.numberOfCells += 1
        self.totalHeight += terrainCell.height

    def draw(self, board_surface):
        for terrainCell in self.terrainCells:
            terrainCell.draw(board_surface)
        if self.selected:
            for redLine in self.redLines:
                redLine.draw(board_surface)

    def selectIsland(self):
        self.selected = True

    def unselectIsland(self):
        self.selected = False

    def getAvgHeight(self):
        return self.totalHeight / self.numberOfCells