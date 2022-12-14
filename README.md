![rvr gamescreen](https://raw.githubusercontent.com/a-abir/rvrRobo/main/images/gamescreen.png)

## Install required libaraies

`pip install pygame --pre`

## Import and setup instructions:

```python
from robot import robo
robo = robo()
```

Example Program:

```python
from robot import robo
robo = robo()       # initialize the robot
robo.setSpeed(.5)   # Set sim speed 50%

robo.message("Hello World!")
robo.paintWhite()   # put white brush down
robo.left()         # turn left
robo.forward(10)    # move forward 10 steps
robo.paintBlack()   # put black brush down
robo.right()        # turn right
robo.forward(10)    # move forward 10 steps
```
   

## Available Commands:

**Movements:** 

 - `setSpeed(0.5)` 
  : *Set operating simulation speed [Ex. 50%]* 

 - `robo.forward()`
   : *Go one step forward.  
   Use forward(number) to do more steps at once.*

 - `robo.backward()`
	: *Go one step backward.  
	Use backward(number) to do more steps at once.*

 - `robo.left()`
	: *Make a quarter turn to the left.  
	Use left(number) to do more steps at once.*

 - `robo.right()`
	: *Make a quarter turn to the right.  
	Use right(number) to do more steps at once.*


**Grab Commands:**

 - `robo.pickUp()`
	: *Get the beacon in front of the robot*

 - `robo.putDown()`
	: *Put a beacon in front of the robot*

 - `robo.eatUp()`
	: *Pick up and destroy the beacon in front*

**Paint Commands:**

 - `robo.paintWhite()`
	: *Put the brush with white paint to the ground*

 - `robo.paintBlack()`
	: *Put the brush with black paint to the ground*

 - `robo.stopPainting()`
	: *Stop painting, hide the brush*

 - `robo.clearPaint()`
	: *Clear paint at the position of the robot*

**Check Environment:**

 - `robo.leftIsClear()`
 - `robo.frontIsClear()`
 - `robo.rightIsClear()`
 - `robo.leftIsObstacle()`
 - `robo.frontIsObstacle()`
 - `robo.rightIsObstacle()`
 - `robo.leftIsBeacon()`
 - `robo.frontIsBeacon()`
 - `robo.rightIsBeacon`
 - `robo.leftIsWhite()`
 - `robo.frontIsWhite()`
 - `robo.rightIsWhite()`
 - `robo.leftIsBlack()`
 - `robo.frontIsBlack()`
 - `robo.rightIsBlack()`

**Message Commands:**

 - `robo.message(f"My robot: {robo}")`
	: *Print all robo info [Ex. Robot(3, 11) | Orientation: 90 | Cargo: 0 | Paint: None]*

 - `robo.message(f"location {robo.loc[0]} , {robo.loc[1]}")`
	: *Insert the current location (x,y)*
	
 - `robo.message(f"{robo.cargo} beacons")`
	: *Insert the number of beacons carried by Robo*

<br>
<br>
<hr>

## Make a custom map

**Keymap:**

    W, w, n, m = walls elements
    .     = empty space (floor)
    R/r   = robot
    1     = white paint
    0     = black paint
    B/b   = beacon

**Custom map Example:**
```python
from robot import robo

exampleMap = [
    "WnWmmWWWWWWWWWWmWWWWWnW",
    "WmWmm.......B.....mmWmW",
    "W..........B..........W",
    "W.........B...........W",
    "W........B............W",
    "W.......B.............W",
    "W......B..............W",
    "W.....B...............W",
    "W....B................W",
    "W...B.................W",
    "W..B...........R......W",
    "W.B...................W",
    "W.....................W",
    "WWWnWWWWmWWWWWWWWnWnnmW"]

robo = robo(exampleMap)
robo.forward(10)
```
![rvr gamescreen](https://raw.githubusercontent.com/a-abir/rvrRobo/main/images/customMap.png)
