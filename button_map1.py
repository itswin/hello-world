import pygame
import sys

pygame.init()
pygame.display.set_mode((100, 100))
pygame.key.set_repeat(50)

done = False

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


while not done:
    # EVENT PROCESSING STEP
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop

    if joystick.get_button(0) == 1: # A
        print("Button 0 pressed")

    if joystick.get_button(1) == 1: # B
        print("Button 1 pressed")

    if joystick.get_button(2) == 1: # X
        print("Button 2 pressed")

    if joystick.get_button(3) == 1: # Y
        print("Button 3 pressed")

    if joystick.get_button(4) == 1: # LB
        print("Button 4 pressed")

    if joystick.get_button(5) == 1: # RB
        print("Button 5 pressed")

    if joystick.get_button(6) == 1: # Back
        print("Button 6 pressed")

    if joystick.get_button(7) == 1: # Start
        print("Button 7 pressed")

    if joystick.get_button(8) == 1: # Press left joystick
        print("Button 8 pressed")

    if joystick.get_button(9) == 1:# Press right joystick
        print("Button 9 pressed")

    if abs(joystick.get_axis(0)) > 0.05 or abs(joystick.get_axis(1)) > 0.05:
        print("Left stick %f, %f" % (joystick.get_axis(0),
                                     joystick.get_axis(1)))

    if abs(joystick.get_axis(3)) > 0.05 or abs(joystick.get_axis(4)) > 0.05:
        print("Right stick %f, %f" % (joystick.get_axis(4),
                                      joystick.get_axis(3)))

    if joystick.get_axis(2) > 0.05:
        print("Left Trigger %f" % (joystick.get_axis(2)))

    if joystick.get_axis(5) > 0.05:
        print("Right Trigger %f" % joystick.get_axis(5))

    (hat_x, hat_y) = joystick.get_hat(0)
    if (hat_x != 0 or hat_y !=0):
        print("Hat %d, %d" % (hat_x, hat_y))


# Close the window and quit.
pygame.quit()
