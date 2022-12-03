import pygame
import sys   
import time 

"""
Author: Abrian Abir
Date: 12/02/2022
Course: EF 230
Description: This is a class that will be used to create a robot object.
"""

pygame.init()
pygame.font.init()

pygame.display.set_caption("Virtual RVR")
my_font = pygame.font.SysFont('consolas', 30)

# 19 x 12 grid
maps = ['WnWmmWWWWWWWWWWmWWWWWnW',
        'WWWWWWWWWWWWWWWWWWWWWWW',
        'WW........1....WmWWmBWW',
        'WW........1....WwWwW.WW',
        'WW..WW....1m...WWWWW.Wn',
        'Wm...WWW....WWWWW.1..WW',
        'Wn....1.....WWWwW.1..WW',
        'WmW...11....WWmWWW1WmWW',
        'WWw...111......WWW1..WW',
        'mWw...111......1.11..WW',
        'WWW...........11.....WW',
        'WWn.................mWW',
        'WW.......Bn..........WW',
        'nWWWWWWWWWWWWWWWnWWWWWW',
        'WWWnWWWWmWWWWWWWWnWnnmW'] 

scales = 50
screenW, screenH = len(maps[0]), len(maps)
screen = pygame.display.set_mode((screenW * scales, screenH * scales))
wall = pygame.image.load("images/wall.png").convert()
wall = pygame.transform.scale(wall, (scales, scales))
wall1 = pygame.image.load("images/wall1.png").convert()
wall1 = pygame.transform.scale(wall1, (scales, scales))
wall2 = pygame.image.load("images/wall2.png").convert()
wall2 = pygame.transform.scale(wall2, (scales, scales))
floor = pygame.image.load("images/floor.png").convert()
floor = pygame.transform.scale(floor, (scales, scales))
beacon = pygame.image.load("images/beacon.png").convert_alpha()
beacon = pygame.transform.scale(beacon, (scales, scales))
water = pygame.image.load("images/water.png").convert()
water = pygame.transform.scale(water, (scales, scales))
white = pygame.image.load("images/white.png").convert()
white = pygame.transform.scale(white, (scales, scales))
black = pygame.image.load("images/black.png").convert()
black = pygame.transform.scale(black, (scales, scales))

class robo():
    def __init__(self, x=9, y=11):
        self.orientation = 0
        self.rect = pygame.rect.Rect((scales*x, scales*y, scales, scales))
        self.loc = (x, y)
        self.cargo = 0
        self.paint = None
        self.__speed = 1
        self.messageTxt = ''
        self.clock = pygame.time.Clock()
        self.image = pygame.image.load("images/spaceship.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (scales, scales))
        self.update()

    def setSpeed(self, speed):
        self.__speed = speed

    def _getFrontElem(self):
        if self.orientation == 0:
            return maps[self.loc[1] - 1][self.loc[0]]
        elif self.orientation == 90:
            return maps[self.loc[1]][self.loc[0] - 1]
        elif self.orientation == 180:
            return maps[self.loc[1] + 1][self.loc[0]]
        elif self.orientation == 270:
            return maps[self.loc[1]][self.loc[0] + 1]
        
    def _getBackElem(self):
        if self.orientation == 0:
            return maps[self.loc[1] + 1][self.loc[0]]
        elif self.orientation == 90:
            return maps[self.loc[1]][self.loc[0] + 1]
        elif self.orientation == 180:
            return maps[self.loc[1] - 1][self.loc[0]]
        elif self.orientation == 270:
            return maps[self.loc[1]][self.loc[0] - 1]

    def _getFrontElemLoc(self):
        if self.orientation == 0:
            return (self.loc[0], self.loc[1] - 1)
        elif self.orientation == 90:
            return (self.loc[0] - 1, self.loc[1])
        elif self.orientation == 180:
            return (self.loc[0], self.loc[1] + 1)
        elif self.orientation == 270:
            return (self.loc[0] + 1, self.loc[1])
    
    def _leftElement(self):
        self.left()
        flem = self._getFrontElem()
        self.right()
        return flem
    
    def _rightElement(self):
        self.right()
        flem = self._getFrontElem()
        self.left()
        return flem

    def message(self, text):
        self.messageTxt = text

    def _getFrontRoboMov(self):
        if self.orientation == 0:
            return (0, -scales)
        elif self.orientation == 90:
            return (-scales, 0)
        elif self.orientation == 180:
            return (0, scales)
        elif self.orientation == 270:
            return (scales, 0)
    
    def forward(self, steps=1, update=True):
        for _ in range(steps):
            if update:
                self.update()
            time.sleep(0.15 / self.__speed)
            if self.frontIsObstacle():
                for i in range(6):
                    time.sleep(0.05 / self.__speed)
                    if i % 2 == 0:
                        self.orientation += 15
                    else:
                        self.orientation -= 15
                    self.update()
                return
            else:
                fmov = self._getFrontRoboMov()
                self.rect.move_ip(*fmov)
                self.loc = (self.loc[0] + fmov[0] // scales, self.loc[1] + fmov[1] // scales)
            if update:
                self.update()
                
    def backward(self, steps=1):
        for _ in range(steps):
            self.update()
            time.sleep(0.15 / self.__speed)
            if self._backIsObstacle():
                for i in range(6):
                    time.sleep(0.05 / self.__speed)
                    if i % 2 == 0:
                        self.orientation += 15
                    else:
                        self.orientation -= 15
                    self.update()
                return
            else:
                fmov = self._getFrontRoboMov()
                self.rect.move_ip(-fmov[0], -fmov[1])
                self.loc = (self.loc[0] - fmov[0] // scales, self.loc[1] - fmov[1] // scales)
            self.update()

    def right(self, steps=1):
        for _ in range(steps):
            self.orientation -= 90
            self.orientation %= 360
            time.sleep(0.15 / self.__speed)
            self.update()

    def left(self, steps=1):
        for _ in range(steps):
            self.orientation += 90
            self.orientation %= 360
            time.sleep(0.15 / self.__speed)
            self.update()

    def pickUp(self):
        flem = self._getFrontElem()
        if flem.lower() == "b":
            self.cargo += 1
            floc = self._getFrontElemLoc()
            maps[floc[1]] = maps[floc[1]][:floc[0]] + "." + maps[floc[1]][floc[0] + 1:]

    def putDown(self):
        if self.cargo == 0:
            return
        if self.frontIsObstacle():
            return
        else:
            self.cargo -= 1
            floc = self._getFrontElemLoc()
            maps[floc[1]] = maps[floc[1]][:floc[0]] + "b" + maps[floc[1]][floc[0] + 1:]

    def eatUp(self):
        if self._getFrontElem().lower() == "b":
            floc = self._getFrontElemLoc()
            maps[floc[1]] = maps[floc[1]][:floc[0]] + "." + maps[floc[1]][floc[0] + 1:]

    def paintWhite(self):
        self.paint = "1"
    
    def paintBlack(self):
        self.paint = "0"

    def stopPainting(self):
        self.paint = None
    
    def leftIsBeacon(self):
        return self._leftElement().lower() == "b"

    def _backIsBeacon(self):
        return self._getBackElem().lower() == "b"

    def frontIsBeacon(self):
        return self._getFrontElem().lower() == "b"

    def rightIsBeacon(self):
        return self._rightElement().lower() == "b"

    def leftIsWall(self):
        return self._leftElement().lower() in ['w', 'n', 'm']

    def _backIsWall(self):
        return self._getBackElem().lower() in ['w', 'n', 'm']

    def frontIsWall(self):
        return self._getFrontElem().lower() in ['w', 'n', 'm']

    def rightIsWall(self):
        return self._rightElement().lower() in ['w', 'n', 'm']

    def leftIsClear(self):
        return not self.leftIsWall() and not self.leftIsBeacon()
    
    def frontIsClear(self):
        return not self.frontIsWall() and not self.frontIsBeacon()

    def rightIsClear(self):
        return not self.rightIsWall() and not self.rightIsBeacon()

    def leftIsObstacle(self):
        return self.leftIsWall() or self.leftIsBeacon()

    def frontIsObstacle(self):
        return self.frontIsWall() or self.frontIsBeacon()
    
    def _backIsObstacle(self):
        return self._backIsWall() or self._backIsBeacon()

    def rightIsObstacle(self):
        return self.rightIsWall() or self.rightIsBeacon()

    def leftIsWhite(self):
        return self._leftElement().lower() == "1"

    def frontIsWhite(self):
        return self._getFrontElem().lower() == "1"

    def rightIsWhite(self):
        return self._rightElement().lower() == "1"

    def leftIsBlack(self):
        return self._leftElement().lower() == "0"

    def frontIsBlack(self):
        return self._getFrontElem().lower() == "0"

    def rightIsBlack(self):
        return self._rightElement().lower() == "0"

    def draw(self, surface) -> None:
        img = pygame.transform.rotate(self.image, self.orientation)
        surface.blit(img, self.rect)

    def drawGrid(self):
        for x in range(0, len(maps[0])):
            for y in range(0, len(maps)):
                if maps[y][x] == "W":
                    screen.blit(wall, (x*scales, y*scales))
                elif maps[y][x] == "w":
                    screen.blit(water, (x*scales, y*scales))
                elif maps[y][x] == "m":
                    screen.blit(wall1, (x*scales, y*scales))
                elif maps[y][x] == "n":
                    screen.blit(wall2, (x*scales, y*scales))
                elif maps[y][x].lower() == "0": 
                    screen.blit(black, (x*scales, y*scales))
                elif maps[y][x].lower() == "1":
                    screen.blit(white, (x*scales, y*scales))
                elif maps[y][x].lower() == "b":
                    screen.blit(beacon, (x*scales, y*scales))
                else:
                    screen.blit(floor, (x*scales, y*scales))

    def update(self):
        self.drawGrid()
        self.draw(screen)
        if len(self.messageTxt) > 0:
            surf = my_font.render(self.messageTxt, False, (0, 0,0))
            pygame.draw.rect(screen, (255, 255, 255), surf.get_rect())
            screen.blit(surf, (0, 0))
        if self.paint != None:
            maps[self.loc[1]] = maps[self.loc[1]][:self.loc[0]] + self.paint + maps[self.loc[1]][self.loc[0] + 1:]
        pygame.display.update()
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
        self.clock.tick(10)


if __name__ == "__main__":
    print("\n\nThis file is not meant to be run directly. \
        \nPlease import it using \"from robot import robo\"")
    sys.exit(1)
