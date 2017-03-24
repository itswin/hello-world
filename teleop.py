def videoCallback( frame, drone, debug=False ):
   global cnt
   if isinstance(frame, tuple):
       print("h.264 frame - (frame# = %s, iframe = %s, size = %s)" % (frame[0],
                                                                      frame[1],
                                                                      len(frame[2])))
       f.write(frame[-1])
       f.flush()
   else:
       cnt = cnt + 1
       cv2.imshow("image", frame)
       cv2.waitKey(10)

def scale(value, scaler):
    if abs(value) < 0.05:
        return 0
    return value * scaler

from bebop import Bebop
from commands import *
import pygame

import cv2

cnt = 0
f = open( "./images/video.h264", "wb" )

print("Connecting to drone...")
drone = Bebop( metalog=None, onlyIFrames=True)
drone.trim()
drone.videoCbk = videoCallback
drone.videoEnable()
print("Connected.")

pygame.init()
size = [100, 100]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Drone Teleop")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Initializes joystick
if pygame.joystick.get_count() == 0:
    print("No joysticks found")
    done = True
else:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print("Initialized %s" % (joystick.get_name()))
    print("Number of buttons %d. Number of axis %d, Number of hats %d" %
          (joystick.get_numbuttons(), joystick.get_numaxes(),
           joystick.get_numhats()))


MAX_SPEED = 50

# -------- Main Program Loop -----------
while not done:
    try:
        # EVENT PROCESSING STEP
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop

        if joystick.get_button(4) == 1:
            print("Landing...")
            if drone.flyingState is None or drone.flyingState == 1: # if taking off then do emegency landing
                drone.emergency()
            drone.land()

        if joystick.get_button(6) == 1:
            drone.land()

        if joystick.get_button(7) == 1:
            if drone.flyingState == 0:
                drone.takeoff()

        (hat_x, hat_y) = joystick.get_hat(0)

        if joystick.get_button(0) == 1 and hat_y == 1:
            print("Executing Front Flip")
            drone.frontFlip()

        if joystick.get_button(0) == 1 and hat_y == -1:
            print("Executing Back Flip")
            drone.backFlip()

        if joystick.get_button(0) == 1 and hat_x == 1:
            print("Executing Right Flip")
            drone.rightFlip()

        if joystick.get_button(0) == 1 and hat_x == -1:
            print("Executing Left Flip")
            drone.leftFlip()

        # Power values
        roll = scale(joystick.get_axis(0), MAX_SPEED)
        pitch = -scale(joystick.get_axis(1), MAX_SPEED)
        yaw = scale(joystick.get_axis(4), MAX_SPEED)
        gaz = -scale(joystick.get_axis(3), MAX_SPEED)

        drone.update(cmd=movePCMDCmd(True, roll, pitch, yaw, gaz))

        # Limit to 20 frames per second
        clock.tick(20)

    except:
        print("Error")
        if drone.flyingState is None or drone.flyingState == 1:
            # if taking off then do emergency landing
            drone.emergency()
        drone.land()

# Close the window and quit.
pygame.quit()
