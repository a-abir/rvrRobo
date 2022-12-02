## Import and setup instructions:

    from robot import robo
    robo = robo()

Example Program:

    from robot import robo
	robo = robo()		# initialize clss
	robo.setSpeed(.5)	# set sim speed 50%
	
	robo.paintWhite()	# put white brush down
	robo.right()
	robo.forward(10)	# forward 10 units
	robo.paintBlack()	# put black brush down
	robo.right()
	robo.forward(10)	# forward 10 units
   

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

 - `robo.message(f"location {robo.loc[0]} , {robo.loc[1]}")`
	: *Insert the current location (x,y)*
	
 - `robo.message(f"{robo.cargo} beacons")`
	: *Insert the number of beacons carried by Robo*
