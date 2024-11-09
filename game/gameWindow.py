from game import randomIslandGenerator
from game.randomIslandGenerator import RandomIslandGenerator
from game.sprites.archipelago import *

class Game:
    def __init__(self):
        pygame.init()  # Initialize pygame
        self.rows = ROWS
        self.cols = COLS
        self.winWidth = WINDOW_WIDTH
        self.winHeight = WINDOW_HEIGHT
        self.running = True

        self.window = pygame.display.set_mode((self.winWidth, self.winHeight))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()

        self.mapFromNordeus = True


    def new(self):
        if self.mapFromNordeus:
            self.boardArchipelago = Archipelago(requests.get(GET_REQ_LINK).text)
        else:
            self.boardArchipelago = Archipelago(RandomIslandGenerator.generate_distinct_islands_map(30,1000,10))
        self.mapFromNordeus = not self.mapFromNordeus


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

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                mouse_x -= MAP_OFFSET_X
                mouse_y -= MAP_OFFSET_Y
                mouse_x //= TILESIZE
                mouse_y //= TILESIZE

                if event.button == 1:
                    # left button click
                    self.boardArchipelago.selectIslandAt(mouse_x, mouse_y)
                else:
                    # right button click
                    self.boardArchipelago.selectIslandAt(mouse_x, mouse_y)

    def update(self):
        pass

    def draw(self):
        if self.running:
            # Only draw if the game is still running
            self.window.fill(WHITE)
            self.boardArchipelago.draw(self.window.subsurface([MAP_OFFSET_X,MAP_OFFSET_Y,MAP_OFFSET_X + WIDTH,MAP_OFFSET_Y + HEIGHT]))
            # Use single flip!
            pygame.display.flip()

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