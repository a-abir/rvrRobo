import pygame
import sys

"""
Author: Abrian Abir
Date: 12/02/2022
Course: EF 230
Description: This is a class that will be used to create a robot object.
"""

pygame.init()
pygame.font.init()

pygame.display.set_caption("Virtual RVR")
_font = pygame.font.SysFont("consolas", 30)

# 19 x 12 grid map
_maps = [
    "WnWmmWWWWWWWWWWmWWWWWnW",
    "WWWWWWWWWWWWWWWWWWWWWWW",
    "WW........1....WmWWmBWW",
    "WW........1....WwWwW.WW",
    "WW..WWmW..1.....WWWW.Wn",
    "Wm...nWW....WW....1..WW",
    "Wn....1.....WwnWW.1..WW",
    "WmW...11....WWmWwW1WmWW",
    "WWw...111......WW.1..WW",
    "mWw...111......1.11..WW",
    "WWW...........11.....WW",
    "WWn.................mWW",
    "WW.......Bn..........WW",
    "nWWWWWWWWWWWWWWWnWWWWWW",
    "WWWnWWWWmWWWWWWWWnWnnmW",
]

_scales = 50
_screenW, _screenH = len(_maps[0]), len(_maps)
_screen = pygame.display.set_mode((_screenW * _scales, _screenH * _scales))


def getSprites(filename, scl, dim=[3, 3]):
    shts = []
    sprt = pygame.image.load(filename).convert_alpha()
    sprt = pygame.transform.scale(sprt, (scl * dim[0], scl * dim[1]))
    for ly in range(0, dim[1] * scl, scl):
        for lx in range(0, dim[0] * scl, scl):
            rct = (lx, ly, scl, scl)
            rct = pygame.Rect(rct)
            img = pygame.Surface(rct.size).convert()
            img.blit(sprt, (0, 0), rct)
            img.set_colorkey((255, 255, 255), pygame.RLEACCEL)
            shts.append(img)
    return shts


# load in images from spritesheet 3x3
_sprites = getSprites("images/sprite.png", _scales, [3, 5])
_beacon, _black, _floor = _sprites[0:3]
_walls = _sprites[4:7]
_water, _white = _sprites[7:9]
_robots = _sprites[9:15]


class robo:
    def __init__(self, x: int = 9, y: int = 11):
        """Robot class constructor

        Arguments:
            x {int} -- x coordinate of robot
            y {int} -- y coordinate of robot
        """
        self.loc = (x, y)
        self.cargo = 0
        self.paint = "None"
        self.__binPaint = None
        self.__orientation: int = 0
        self.__rect = pygame.rect.Rect((_scales * x, _scales * y, _scales, _scales))
        self.__speed = 1
        self.__messageTxt = ""
        self.__robot_iter = [0, 0]
        self.__robot = _robots[self.__robot_iter[0]]
        self.__update()

    def __repr__(self) -> str:
        """Internal function | `Do not call from outside`"""
        return (
            f"Robot({self.loc[0]}, {self.loc[1]}) | Orientation: "
            + f"{self.__orientation} | Cargo: {self.cargo} | Paint: {self.paint}"
        )

    def __str__(self) -> str:
        return self.__repr__()

    def setSpeed(self, speed: float):
        """Set the speed of the robot

        Arguments:
            speed {float} -- speed of the robot
        Usage: `robo.setSpeed(0.5)`
        """
        self.__speed = speed
        self.__update()

    def __getFrontElem(self):
        """Internal function | `Do not call from outside`"""
        if self.__orientation == 0:
            return _maps[self.loc[1] - 1][self.loc[0]]
        elif self.__orientation == 90:
            return _maps[self.loc[1]][self.loc[0] - 1]
        elif self.__orientation == 180:
            return _maps[self.loc[1] + 1][self.loc[0]]
        elif self.__orientation == 270:
            return _maps[self.loc[1]][self.loc[0] + 1]

    def __getBackElem(self):
        """Internal function | `Do not call from outside`"""
        if self.__orientation == 0:
            return _maps[self.loc[1] + 1][self.loc[0]]
        elif self.__orientation == 90:
            return _maps[self.loc[1]][self.loc[0] + 1]
        elif self.__orientation == 180:
            return _maps[self.loc[1] - 1][self.loc[0]]
        elif self.__orientation == 270:
            return _maps[self.loc[1]][self.loc[0] - 1]

    def __getFrontElemLoc(self):
        """Internal function | `Do not call from outside`"""
        if self.__orientation == 0:
            return (self.loc[0], self.loc[1] - 1)
        elif self.__orientation == 90:
            return (self.loc[0] - 1, self.loc[1])
        elif self.__orientation == 180:
            return (self.loc[0], self.loc[1] + 1)
        elif self.__orientation == 270:
            return (self.loc[0] + 1, self.loc[1])

    def __leftElement(self) -> str | None:
        """Internal function | `Do not call from outside`"""
        self.left()
        flem = self.__getFrontElem()
        self.right()
        return flem

    def __rightElement(self) -> str | None:
        """Internal function | `Do not call from outside`"""
        self.right()
        flem = self.__getFrontElem()
        self.left()
        return flem

    def __getFrontRoboMov(self):
        """Internal function | `Do not call from outside`"""
        if self.__orientation == 0:
            return (0, -_scales)
        elif self.__orientation == 90:
            return (-_scales, 0)
        elif self.__orientation == 180:
            return (0, _scales)
        elif self.__orientation == 270:
            return (_scales, 0)

    def message(self, text) -> None:
        """Write a message on the screen

        Arguments:
            text {str} -- message to be displayed
        Usage: `robo.message("Hello World")`
        """
        self.__messageTxt = text
        self.__update()


    def forward(self, steps=1) -> None:
        """Move the robot forward

        Keyword Arguments:
            steps {int} -- number of steps to move (default: {1})
        Usage: `robo.forward()`
        """
        for _ in range(steps):
            self.__update()
            pygame.time.wait(int(25 / self.__speed))
            if self.frontIsObstacle():
                for i in range(6):
                    pygame.time.wait(int(50 / self.__speed))
                    if i % 2 == 0:
                        self.__orientation += 15
                    else:
                        self.__orientation -= 15
                    self.__update()
                return self
            else:
                fmov = self.__getFrontRoboMov()
                for _ in range(_scales):
                    self.__rect.move_ip(fmov[0] // _scales, fmov[1] // _scales)
                    pygame.time.wait(2)
                    self.__update()
                self.loc = [
                    self.loc[0] + fmov[0] // _scales,
                    self.loc[1] + fmov[1] // _scales,
                ]
            self.__update()
        return self

    def backward(self, steps=1) -> None:
        """Move the robot backward

        Keyword Arguments:
            steps {int} -- number of steps to move (default: {1})
        Usage: `robo.backward()`
        """
        for _ in range(steps):
            self.__update()
            pygame.time.wait(int(100 / self.__speed))
            if self.__backIsObstacle():
                for i in range(6):
                    pygame.time.wait(int(50 / self.__speed))
                    if i % 2 == 0:
                        self.__orientation += 15
                    else:
                        self.__orientation -= 15
                    self.__update()
                return self
            else:
                fmov = self.__getFrontRoboMov()
                for _ in range(_scales):
                    self.__rect.move_ip(-fmov[0] // _scales, -fmov[1] // _scales)
                    self.__update()
                self.loc = [
                    self.loc[0] - fmov[0] // _scales,
                    self.loc[1] - fmov[1] // _scales,
                ]
            self.__update()
        return self

    def right(self, steps=1):
        """Turn the robot right

        Keyword Arguments:
            steps {int} -- number of steps to move (default: {1})
        Usage: `robo.right()`
        """
        for _ in range(steps):
            for _ in range(45):
                self.__orientation -= 2
                self.__update()
            self.__orientation %= 360
            self.__update()
        return self

    def left(self, steps=1):
        """Turn the robot left

        Keyword Arguments:
            steps {int} -- number of steps to move (default: {1})
        Usage: `robo.left()`
        """
        for _ in range(steps):
            for _ in range(45):
                self.__orientation += 2
                self.__update()
            self.__orientation %= 360
            self.__update()
        return self

    def pickUp(self):
        """Pick up the object in front of the robot
        Usage: `robo.pickUp()`
        """
        flem = self.__getFrontElem()
        if flem.lower() == "b":
            pygame.time.wait(int(150 / self.__speed))
            self.cargo += 1
            floc = self.__getFrontElemLoc()
            _maps[floc[1]] = (
                _maps[floc[1]][: floc[0]] + "." + _maps[floc[1]][floc[0] + 1 :]
            )
            self.__update()
        return self

    def putDown(self):
        """Put down the object in front of the robot
        Usage: `robo.putDown()`
        """
        if self.cargo == 0:
            return self
        if self.frontIsObstacle():
            return self
        else:
            pygame.time.wait(int(150 // self.__speed))
            self.cargo -= 1
            floc = self.__getFrontElemLoc()
            _maps[floc[1]] = (
                _maps[floc[1]][: floc[0]] + "b" + _maps[floc[1]][floc[0] + 1 :]
            )
            self.__update()
        return self

    def eatUp(self):
        """Eat up the object in front of the robot
        Usage: `robo.eatUp()`
        """
        if self.__getFrontElem().lower() == "b":
            pygame.time.wait(int(150 // self.__speed))
            floc = self.__getFrontElemLoc()
            _maps[floc[1]] = (
                _maps[floc[1]][: floc[0]] + "." + _maps[floc[1]][floc[0] + 1 :]
            )
            self.__update()
        return self

    def paintWhite(self):
        """Paint the object in front of the robot white
        Usage: `robo.paintWhite()`
        """
        self.__binPaint = "1"
        self.paint = "White"
        return self

    def paintBlack(self):
        """Paint the object in front of the robot black
        Usage: `robo.paintBlack()`
        """
        self.__binPaint = "0"
        self.paint = "Black"
        return self

    def stopPainting(self):
        """Stop painting the object in front of the robot
        Usage: `robo.stopPainting()`
        """
        self.__binPaint = None
        self.paint = "None"
        return self

    def clearPaint(self):
        """Clear the paint on the object in front of the robot
        Usage: `robo.clearPaint()`
        """
        if (
            _maps[self.loc[1]][self.loc[0]] == "1"
            or _maps[self.loc[1]][self.loc[0]] == "0"
        ):
            _maps[self.loc[1]] = (
                _maps[self.loc[1]][: self.loc[0]]
                + "."
                + _maps[self.loc[1]][self.loc[0] + 1 :]
            )
            self.__update()
        return self

    def leftIsBeacon(self):
        """Check if the object on the left is a beacon
        Usage: `robo.leftIsBeacon()`
        """
        return self.__leftElement().lower() == "b"

    def __backIsBeacon(self):
        """Internal function | `Do not call from outside`"""
        return self.__getBackElem().lower() == "b"

    def frontIsBeacon(self):
        """Check if the object in front is a beacon
        Usage: `robo.frontIsBeacon()`
        """
        return self.__getFrontElem().lower() == "b"

    def rightIsBeacon(self):
        """Check if the object on the right is a beacon
        Usage: `robo.rightIsBeacon()`
        """
        return self.__rightElement().lower() == "b"

    def leftIsWall(self):
        """Check if the object on the left is a wall
        Usage: `robo.leftIsWall()`
        """
        return self.__leftElement().lower() in ["w", "n", "m"]

    def __backIsWall(self):
        """Internal function | `Do not call from outside`"""
        return self.__getBackElem().lower() in ["w", "n", "m"]

    def frontIsWall(self):
        """Check if the object in front is a wall
        Usage: `robo.frontIsWall()`
        """
        return self.__getFrontElem().lower() in ["w", "n", "m"]

    def rightIsWall(self):
        """Check if the object on the right is a wall
        Usage: `robo.rightIsWall()`
        """
        return self.__rightElement().lower() in ["w", "n", "m"]

    def leftIsClear(self):
        """Check if the object on the left is clear
        Usage: `robo.leftIsClear()`
        """
        return not self.leftIsWall() and not self.leftIsBeacon()

    def frontIsClear(self):
        """Check if the object in front is clear
        Usage: `robo.frontIsClear()`
        """
        return not self.frontIsWall() and not self.frontIsBeacon()

    def rightIsClear(self):
        """Check if the object on the right is clear
        Usage: `robo.rightIsClear()`
        """
        return not self.rightIsWall() and not self.rightIsBeacon()

    def leftIsObstacle(self):
        """Check if the object on the left is an obstacle
        Usage: `robo.leftIsObstacle()`
        """
        return self.leftIsWall() or self.leftIsBeacon()

    def frontIsObstacle(self):
        """Check if the object in front is an obstacle
        Usage: `robo.frontIsObstacle()`
        """
        return self.frontIsWall() or self.frontIsBeacon()

    def __backIsObstacle(self):
        """Internal function | `Do not call from outside`"""
        return self.__backIsWall() or self.__backIsBeacon()

    def rightIsObstacle(self):
        """Check if the object on the right is an obstacle
        Usage: `robo.rightIsObstacle()`
        """
        return self.rightIsWall() or self.rightIsBeacon()

    def leftIsWhite(self):
        """Check if the object on the left is white
        Usage: `robo.leftIsWhite()`
        """
        return self.__leftElement().lower() == "1"

    def frontIsWhite(self):
        """Check if the object in front is white
        Usage: `robo.frontIsWhite()`
        """
        return self.__getFrontElem().lower() == "1"

    def rightIsWhite(self):
        """Check if the object on the right is white
        Usage: `robo.rightIsWhite()`
        """
        return self.__rightElement().lower() == "1"

    def leftIsBlack(self):
        """Check if the object on the left is black
        Usage: `robo.leftIsBlack()`
        """
        return self.__leftElement().lower() == "0"

    def frontIsBlack(self):
        """Check if the object in front is black
        Usage: `robo.frontIsBlack()`
        """
        return self.__getFrontElem().lower() == "0"

    def rightIsBlack(self):
        """Check if the object on the right is black
        Usage: `robo.rightIsBlack()`
        """
        return self.__rightElement().lower() == "0"

    def __draw(self, surface) -> None:
        """Internal function | `Do not call from outside`"""
        self.__robot_iter[1] += 1
        if self.__robot_iter[1] >= 4:
            self.__robot_iter[1] = 0
            self.__robot_iter[0] += 1
            if self.__robot_iter[0] >= len(_robots):
                self.__robot_iter[0] = 0
            self.__robot = _robots[self.__robot_iter[0]]

        img = pygame.transform.rotate(self.__robot, self.__orientation)
        surface.blit(img, self.__rect)

    def __drawGrid(self):
        """Internal function | `Do not call from outside`"""
        for x in range(0, len(_maps[0])):
            for y in range(0, len(_maps)):
                if _maps[y][x] == "W":
                    _screen.blit(_walls[0], (x * _scales, y * _scales))
                elif _maps[y][x] == "w":
                    _screen.blit(_water, (x * _scales, y * _scales))
                elif _maps[y][x] == "m":
                    _screen.blit(_walls[1], (x * _scales, y * _scales))
                elif _maps[y][x] == "n":
                    _screen.blit(_walls[2], (x * _scales, y * _scales))
                elif _maps[y][x].lower() == "0":
                    _screen.blit(_black, (x * _scales, y * _scales))
                elif _maps[y][x].lower() == "1":
                    _screen.blit(_white, (x * _scales, y * _scales))
                elif _maps[y][x].lower() == "b":
                    _screen.blit(_beacon, (x * _scales, y * _scales))
                else:
                    _screen.blit(_floor, (x * _scales, y * _scales))

    def __update(self):
        """Internal function | `Do not call from outside`"""
        self.__drawGrid()
        self.__draw(_screen)
        if len(self.__messageTxt) > 0:
            surf = _font.render(self.__messageTxt, False, (0, 0, 0))
            pygame.draw.rect(_screen, (255, 255, 255), surf.get_rect())
            _screen.blit(surf, (0, 0))
        if self.__binPaint != None:
            _maps[self.loc[1]] = (
                _maps[self.loc[1]][: self.loc[0]]
                + self.__binPaint
                + _maps[self.loc[1]][self.loc[0] + 1 :]
            )
        pygame.display.update()
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)


if __name__ == "__main__":
    print(
        '\n\nThis file is not meant to be run directly. \
        \nPlease import it using "from robot import robo"'
    )
    sys.exit(1)
