from game.sprites.archipelago import *

class Game:
    def __init__(self):
        pygame.init()  # Initialize pygame
        self.rows = ROWS
        self.cols = COLS
        self.winWidth = WIDTH
        self.winHeight = HEIGHT
        self.running = True

        self.window = pygame.display.set_mode((self.winWidth, self.winHeight))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()

    def new(self):
        self.board = Archipelago(requests.get("https://jobfair.nordeus.com/jf24-fullstack-challenge/test").text)
        #self.board.display_board()

    def __str__(self):
        return f"Grid which has {self.rows} rows and {self.cols} cols, winSize = {self.winWidth} x {self.winHeight}"

    def run(self):
        self.running = True
        while self.running:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        pass

    def draw(self):
        if self.running:  # Only draw if the game is still running
            self.window.fill(BGCOLOUR)
            #self.drawGrid()
            self.board.draw(self.window)
            pygame.display.flip()  # Use single flip instead of update

    def drawGrid(self):
        offsetFromTop = 50
        distanceBtwRows = self.winHeight // self.rows
        distanceBtwCols = self.winWidth // self.cols
        x = 0
        y = offsetFromTop
        for i in range(self.rows):
            x += distanceBtwRows
            pygame.draw.line(self.window, WHITE, (x, offsetFromTop), (x, self.winHeight), 2)
            pygame.draw.line(self.window, WHITE, (0, y), (self.winWidth, y), 2)
            y += distanceBtwCols


def main():
    game = Game()
    while 1:
        game.new()
        game.run()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()