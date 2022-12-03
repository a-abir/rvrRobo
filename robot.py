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
_font_ = pygame.font.SysFont("consolas", 30)

# 19 x 12 grid map
_maps_ = [
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

_scales_ = 50
_screenW_, _screenH_ = len(_maps_[0]), len(_maps_)
_screen_ = pygame.display.set_mode((_screenW_ * _scales_, _screenH_ * _scales_))


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
_sprites_ = getSprites("images/sprite.png", _scales_, [3, 5])
_beacon_, _black_, _floor_ = _sprites_[0:3]
_walls_ = _sprites_[4:7]
_water_, _white_ = _sprites_[7:9]
_robots_ = _sprites_[9:15]


class robo:
    def __init__(self, x: int = 9, y: int = 11):
        """Robot class constructor

        Arguments:
            x {int} -- x coordinate of robot
            y {int} -- y coordinate of robot
        """
        self.loc = (x, y)
        self.cargo = 0
        self.paint = None
        self._orientation_: int = 0
        self._rect_ = pygame.rect.Rect((_scales_ * x, _scales_ * y, _scales_, _scales_))
        self._speed = 1
        self._messageTxt_ = ""
        self._robot_iter_ = [0, 0]
        self._robot_ = _robots_[self._robot_iter_[0]]
        self.__update__()

    def setSpeed(self, speed: float):
        """Set the speed of the robot

        Arguments:
            speed {float} -- speed of the robot
        Usage: `robo.setSpeed(0.5)`
        """
        self._speed = speed
        self.__update__()

    def __getFrontElem__(self):
        """Internal function | `Do not call from outside`"""
        if self._orientation_ == 0:
            return _maps_[self.loc[1] - 1][self.loc[0]]
        elif self._orientation_ == 90:
            return _maps_[self.loc[1]][self.loc[0] - 1]
        elif self._orientation_ == 180:
            return _maps_[self.loc[1] + 1][self.loc[0]]
        elif self._orientation_ == 270:
            return _maps_[self.loc[1]][self.loc[0] + 1]

    def __getBackElem__(self):
        """Internal function | `Do not call from outside`"""
        if self._orientation_ == 0:
            return _maps_[self.loc[1] + 1][self.loc[0]]
        elif self._orientation_ == 90:
            return _maps_[self.loc[1]][self.loc[0] + 1]
        elif self._orientation_ == 180:
            return _maps_[self.loc[1] - 1][self.loc[0]]
        elif self._orientation_ == 270:
            return _maps_[self.loc[1]][self.loc[0] - 1]

    def __getFrontElemLoc__(self):
        """Internal function | `Do not call from outside`"""
        if self._orientation_ == 0:
            return (self.loc[0], self.loc[1] - 1)
        elif self._orientation_ == 90:
            return (self.loc[0] - 1, self.loc[1])
        elif self._orientation_ == 180:
            return (self.loc[0], self.loc[1] + 1)
        elif self._orientation_ == 270:
            return (self.loc[0] + 1, self.loc[1])

    def __leftElement__(self) -> str | None:
        """Internal function | `Do not call from outside`"""
        self.left()
        flem = self.__getFrontElem__()
        self.right()
        return flem

    def __rightElement__(self) -> str | None:
        """Internal function | `Do not call from outside`"""
        self.right()
        flem = self.__getFrontElem__()
        self.left()
        return flem

    def message(self, text) -> None:
        """Write a message on the screen

        Arguments:
            text {str} -- message to be displayed
        Usage: `robo.message("Hello World")`
        """
        self._messageTxt_ = text
        self.__update__()

    def __getFrontRoboMov__(self):
        """Internal function | `Do not call from outside`"""
        if self._orientation_ == 0:
            return (0, -_scales_)
        elif self._orientation_ == 90:
            return (-_scales_, 0)
        elif self._orientation_ == 180:
            return (0, _scales_)
        elif self._orientation_ == 270:
            return (_scales_, 0)

    def forward(self, steps=1, update=True) -> None:
        """Move the robot forward

        Keyword Arguments:
            steps {int} -- number of steps to move (default: {1})
            update {bool} -- update the screen (default: {True})
        Usage: `robo.forward()`
        """
        for _ in range(steps):
            if update:
                self.__update__()
            pygame.time.wait(int(25 / self._speed))
            if self.frontIsObstacle():
                for i in range(6):
                    pygame.time.wait(int(50 / self._speed))
                    if i % 2 == 0:
                        self._orientation_ += 15
                    else:
                        self._orientation_ -= 15
                    self.__update__()
                return
            else:
                fmov = self.__getFrontRoboMov__()
                for _ in range(_scales_):
                    self._rect_.move_ip(fmov[0] // _scales_, fmov[1] // _scales_)
                    pygame.time.wait(2)
                    self.__update__()
                self.loc = [
                    self.loc[0] + fmov[0] // _scales_,
                    self.loc[1] + fmov[1] // _scales_,
                ]
            if update:
                self.__update__()

    def backward(self, steps=1) -> None:
        """Move the robot backward

        Keyword Arguments:
            steps {int} -- number of steps to move (default: {1})
        Usage: `robo.backward()`
        """
        for _ in range(steps):
            self.__update__()
            pygame.time.wait(int(100 / self._speed))
            if self.__backIsObstacle__():
                for i in range(6):
                    pygame.time.wait(int(50 / self._speed))
                    if i % 2 == 0:
                        self._orientation_ += 15
                    else:
                        self._orientation_ -= 15
                    self.__update__()
                return
            else:
                fmov = self.__getFrontRoboMov__()
                for _ in range(_scales_):
                    self._rect_.move_ip(-fmov[0] // _scales_, -fmov[1] // _scales_)
                    self.__update__()
                self.loc = [
                    self.loc[0] - fmov[0] // _scales_,
                    self.loc[1] - fmov[1] // _scales_,
                ]
            self.__update__()

    def right(self, steps=1):
        """Turn the robot right

        Keyword Arguments:
            steps {int} -- number of steps to move (default: {1})
        Usage: `robo.right()`
        """
        for _ in range(steps):
            for _ in range(45):
                self._orientation_ -= 2
                self.__update__()
            self._orientation_ %= 360
            self.__update__()

    def left(self, steps=1):
        """Turn the robot left

        Keyword Arguments:
            steps {int} -- number of steps to move (default: {1})
        Usage: `robo.left()`
        """
        for _ in range(steps):
            for _ in range(45):
                self._orientation_ += 2
                self.__update__()
            self._orientation_ %= 360
            self.__update__()

    def pickUp(self):
        """Pick up the object in front of the robot
        Usage: `robo.pickUp()`
        """
        flem = self.__getFrontElem__()
        if flem.lower() == "b":
            pygame.time.wait(int(150 / self._speed))
            self.cargo += 1
            floc = self.__getFrontElemLoc__()
            _maps_[floc[1]] = (
                _maps_[floc[1]][: floc[0]] + "." + _maps_[floc[1]][floc[0] + 1 :]
            )
            self.__update__()

    def putDown(self):
        """Put down the object in front of the robot
        Usage: `robo.putDown()`
        """
        if self.cargo == 0:
            return
        if self.frontIsObstacle():
            return
        else:
            pygame.time.wait(int(150 // self._speed))
            self.cargo -= 1
            floc = self.__getFrontElemLoc__()
            _maps_[floc[1]] = (
                _maps_[floc[1]][: floc[0]] + "b" + _maps_[floc[1]][floc[0] + 1 :]
            )
            self.__update__()

    def eatUp(self):
        """Eat up the object in front of the robot
        Usage: `robo.eatUp()`
        """
        if self.__getFrontElem__().lower() == "b":
            pygame.time.wait(int(150 // self._speed))
            floc = self.__getFrontElemLoc__()
            _maps_[floc[1]] = (
                _maps_[floc[1]][: floc[0]] + "." + _maps_[floc[1]][floc[0] + 1 :]
            )
            self.__update__()

    def paintWhite(self):
        """Paint the object in front of the robot white
        Usage: `robo.paintWhite()`
        """
        self.paint = "1"

    def paintBlack(self):
        """Paint the object in front of the robot black
        Usage: `robo.paintBlack()`
        """
        self.paint = "0"

    def stopPainting(self):
        """Stop painting the object in front of the robot
        Usage: `robo.stopPainting()`
        """
        self.paint = None

    def clearPaint(self):
        """Clear the paint on the object in front of the robot
        Usage: `robo.clearPaint()`
        """
        if (
            _maps_[self.loc[1]][self.loc[0]] == "1"
            or _maps_[self.loc[1]][self.loc[0]] == "0"
        ):
            _maps_[self.loc[1]] = (
                _maps_[self.loc[1]][: self.loc[0]]
                + "."
                + _maps_[self.loc[1]][self.loc[0] + 1 :]
            )
            self.__update__()

    def leftIsBeacon(self):
        """Check if the object on the left is a beacon
        Usage: `robo.leftIsBeacon()`
        """
        return self.__leftElement__().lower() == "b"

    def __backIsBeacon__(self):
        """Internal function | `Do not call from outside`"""
        return self.__getBackElem__().lower() == "b"

    def frontIsBeacon(self):
        """Check if the object in front is a beacon
        Usage: `robo.frontIsBeacon()`
        """
        return self.__getFrontElem__().lower() == "b"

    def rightIsBeacon(self):
        """Check if the object on the right is a beacon
        Usage: `robo.rightIsBeacon()`
        """
        return self.__rightElement__().lower() == "b"

    def leftIsWall(self):
        """Check if the object on the left is a wall
        Usage: `robo.leftIsWall()`
        """
        return self.__leftElement__().lower() in ["w", "n", "m"]

    def __backIsWall__(self):
        """Internal function | `Do not call from outside`"""
        return self.__getBackElem__().lower() in ["w", "n", "m"]

    def frontIsWall(self):
        """Check if the object in front is a wall
        Usage: `robo.frontIsWall()`
        """
        return self.__getFrontElem__().lower() in ["w", "n", "m"]

    def rightIsWall(self):
        """Check if the object on the right is a wall
        Usage: `robo.rightIsWall()`
        """
        return self.__rightElement__().lower() in ["w", "n", "m"]

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

    def __backIsObstacle__(self):
        """Internal function | `Do not call from outside`"""
        return self.__backIsWall__() or self.__backIsBeacon__()

    def rightIsObstacle(self):
        """Check if the object on the right is an obstacle
        Usage: `robo.rightIsObstacle()`
        """
        return self.rightIsWall() or self.rightIsBeacon()

    def leftIsWhite(self):
        """Check if the object on the left is white
        Usage: `robo.leftIsWhite()`
        """
        return self.__leftElement__().lower() == "1"

    def frontIsWhite(self):
        """Check if the object in front is white
        Usage: `robo.frontIsWhite()`
        """
        return self.__getFrontElem__().lower() == "1"

    def rightIsWhite(self):
        """Check if the object on the right is white
        Usage: `robo.rightIsWhite()`
        """
        return self.__rightElement__().lower() == "1"

    def leftIsBlack(self):
        """Check if the object on the left is black
        Usage: `robo.leftIsBlack()`
        """
        return self.__leftElement__().lower() == "0"

    def frontIsBlack(self):
        """Check if the object in front is black
        Usage: `robo.frontIsBlack()`
        """
        return self.__getFrontElem__().lower() == "0"

    def rightIsBlack(self):
        """Check if the object on the right is black
        Usage: `robo.rightIsBlack()`
        """
        return self.__rightElement__().lower() == "0"

    def __draw__(self, surface) -> None:
        """Internal function | `Do not call from outside`"""
        self._robot_iter_[1] += 1
        if self._robot_iter_[1] >= 4:
            self._robot_iter_[1] = 0
            self._robot_iter_[0] += 1
            if self._robot_iter_[0] >= len(_robots_):
                self._robot_iter_[0] = 0
            self._robot_ = _robots_[self._robot_iter_[0]]

        img = pygame.transform.rotate(self._robot_, self._orientation_)
        surface.blit(img, self._rect_)

    def __drawGrid__(self):
        """Internal function | `Do not call from outside`"""
        for x in range(0, len(_maps_[0])):
            for y in range(0, len(_maps_)):
                if _maps_[y][x] == "W":
                    _screen_.blit(_walls_[0], (x * _scales_, y * _scales_))
                elif _maps_[y][x] == "w":
                    _screen_.blit(_water_, (x * _scales_, y * _scales_))
                elif _maps_[y][x] == "m":
                    _screen_.blit(_walls_[1], (x * _scales_, y * _scales_))
                elif _maps_[y][x] == "n":
                    _screen_.blit(_walls_[2], (x * _scales_, y * _scales_))
                elif _maps_[y][x].lower() == "0":
                    _screen_.blit(_black_, (x * _scales_, y * _scales_))
                elif _maps_[y][x].lower() == "1":
                    _screen_.blit(_white_, (x * _scales_, y * _scales_))
                elif _maps_[y][x].lower() == "b":
                    _screen_.blit(_beacon_, (x * _scales_, y * _scales_))
                else:
                    _screen_.blit(_floor_, (x * _scales_, y * _scales_))

    def __update__(self):
        """Internal function | `Do not call from outside`"""
        self.__drawGrid__()
        self.__draw__(_screen_)
        if len(self._messageTxt_) > 0:
            surf = _font_.render(self._messageTxt_, False, (0, 0, 0))
            pygame.draw.rect(_screen_, (255, 255, 255), surf.get_rect())
            _screen_.blit(surf, (0, 0))
        if self.paint != None:
            _maps_[self.loc[1]] = (
                _maps_[self.loc[1]][: self.loc[0]]
                + self.paint
                + _maps_[self.loc[1]][self.loc[0] + 1 :]
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
