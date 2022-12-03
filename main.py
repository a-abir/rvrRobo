from robot import robo

customMap = [
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
    "W..B........R.........W",
    "W.B...................W",
    "W.....................W",
    "WWWnWWWWmWWWWWWWWnWnnmW"]

robo = robo(customMap)  # initialize the robot
robo.setSpeed(.5)       # Set sim speed 50%     

robo.message("Hello")   # display message on screen
robo.paintWhite()       # put white brush down
robo.left()             # turn right
robo.forward(10)        # move forward 10 steps
robo.paintBlack()       # put black brush down
robo.pickUp()           # pick up beacon
robo.backward(10)       # move backward 10 steps
robo.putDown()          # put down beacon
robo.right(10)          # turn right 10 times

