from robot import robo

robo = robo()       # initialize the robot
robo.setSpeed(.5)   # Set sim speed 50%

robo.message("Hello World!")
robo.paintWhite()   # put white brush down
robo.left()         # turn left
robo.left()         # turn left
robo.pickUp()       # pick up cargo
robo.left()        # turn right
robo.backward(10)    # move forward 10 steps
robo.paintBlack()   # put black brush down
robo.left()        # turn right
robo.forward(3)    # move forward 10 steps
robo.putDown()      # put down cargo
robo.right(10)        # turn right

