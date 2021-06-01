# Random map generation
import random, pygame, sys

class Tile:
    collection=[]
    def __init__(self, number, left, right, top, bottom):
        """
        number = grid number
        direction = - FULL / NONE
                    - LEFT / RIGHT
                    - TOP / BOTTOM
        """
        self.number=number
        self.LEFT=left
        self.RIGHT=right
        self.TOP=top
        self.BOTTOM=bottom
        Tile.collection.append(self)

    def __repr__(self):
        return f"<Tile N°{self.number}>"
    def opposite(side):
        return {
        "TOP":"BOTTOM",
        "BOTTOM":"TOP",
        "LEFT":"RIGHT",
        "RIGHT":"LEFT",
        "FULL":"FULL"
        }[side]

    def needed(self, direction):
        return (Tile.opposite(direction),getattr(self, direction))

    def available(self, direction):
        side, state=self.needed(direction)
        correct=[i for i in Tile.collection if getattr(i, side)==state]

    def new(main, x,y):
        if y==0:
            if x==0:
                correct=[i for i in Tile.collection if getattr(i,"BOTTOM")!="NONE" and getattr(i, "RIGHT")!="NONE"]
            else:
                left_tile=[i for i in Tile.collection if i.number==main.map[-1][-1]][0]
                correct=[i for i in Tile.collection if getattr(i, "LEFT")==getattr(left_tile, "RIGHT")]
        else:
            top_tile=[i for i in Tile.collection if i.number==main.map[-2][x]][0]
            if x==0:
                correct=[i for i in Tile.collection if getattr(i, "TOP")==getattr(top_tile, "BOTTOM")]
            else:
                left_tile=[i for i in Tile.collection if i.number==main.map[-1][-1]][0]
                correct=[i for i in Tile.collection if getattr(i, "LEFT")==getattr(left_tile, "RIGHT") and getattr(i, "TOP")==getattr(top_tile, "BOTTOM")]
        return random.choice(correct).number if correct else 17

class Display:
    def __init__(self, grid=False):
        self.tile, self.size=64,15
        self.floor=pygame.image.load("floor.png")
        self.grid=grid
        self.generate_map()

    def generate_map(self):
        self.map=[]
        for y in range(self.size):
            self.map.append([])
            for x in range(self.size):
                self.map[-1].append(Tile.new(self, x,y))

    def load(self):
        self.screen=pygame.display.set_mode((self.tile*self.size,)*2)
        while True:
            self.event()
            self.render()

    def event(self):
        for e in pygame.event.get():
            if e.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif e.type==pygame.KEYDOWN:
                self.generate_map()

    def render(self):
        self.screen.fill((0,0,0))
        for y in range(self.size):
            for x in range(self.size):
                tile=self.map[y][x]-1
                i,j=(tile%4, tile//4)
                rect=pygame.Rect(i*self.tile, j*self.tile, self.tile, self.tile)
                self.screen.blit(self.floor, [e*self.tile for e in (x,y)], rect)
        if self.grid:
            for i in range(1, self.size):
                pygame.draw.line(self.screen, (0,0,0), (0,i*self.tile), (self.tile*self.size, i*self.tile))
                pygame.draw.line(self.screen, (0,0,0), (i*self.tile,0), (i*self.tile, self.tile*self.size))
        pygame.display.update()

if __name__=="__main__":
    Tile(1,"FULL","TOP","FULL", "LEFT")
    Tile(2, "TOP", "FULL", "FULL", "RIGHT")
    Tile(3, "NONE", "BOTTOM", "NONE", "RIGHT")
    Tile(4, "BOTTOM", "NONE", "NONE", "LEFT")
    Tile(5, "FULL", "BOTTOM", "LEFT", "FULL")
    Tile(6, "BOTTOM", "FULL", "RIGHT", "FULL")
    Tile(7, "NONE","TOP", "RIGHT", "NONE")
    Tile(8, "TOP", "NONE", "LEFT", "NONE")
    Tile(9, "FULL", "FULL", "FULL", "FULL")
    for i in range(40): #Get more full dirt tiles
        Tile(10, "FULL", "FULL", "FULL", "FULL")
    Tile(11, "BOTTOM", "BOTTOM", "NONE", "FULL")
    Tile(12, "NONE", "FULL", "RIGHT", "RIGHT")
    Tile(13, "TOP", "BOTTOM", "LEFT", "RIGHT")
    Tile(14, "BOTTOM", "TOP", "RIGHT", "LEFT")
    Tile(15, "TOP", "TOP", "FULL", "NONE")
    Tile(16, "FULL", "NONE", "LEFT", "LEFT")
    Tile(17, "NONE", "NONE", "NONE", "NONE")

    display=Display(True)
    display.load()
