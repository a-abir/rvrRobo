from robot import robo

robo = robo()       # initialize the robot
robo.setSpeed(.5)   # Set sim speed 50%

robo.paintWhite()   # put white brush down
robo.message(f"robo: {robo}")
robo.left(2)        # turn left 2 seconds
robo.pickUp()       # pick up cargo
robo.message("Picked up cargo")
robo.message(f"{robo.cargo} beacons")
robo.right()        # turn right
robo.forward(10)    # move forward 10 steps
robo.message("Moved forward 10 steps")
robo.paintBlack()   # put black brush down
robo.message("Painted black")
robo.right()        # turn right
robo.forward(3)    # move forward 10 steps
robo.message("Moved forward 3 steps")
robo.putDown()      # put down cargo
robo.message("Put down cargo")
robo.stopPainting() # stop painting
robo.clearPaint()   # clear paint
robo.right(5)        # turn right
