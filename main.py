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

