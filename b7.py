import pygame
from pygame.locals import *
from sys import exit
from bluepy import btle
import math
import struct
import BB8_driver

bb8 = BB8_driver.Sphero()
bb8.connect()
#Dualshock4 key codes:
#joystick.get_button(0) - Square
#joystick.get_button(1) - X
#joystick.get_button(2) - O
#joystick.get_button(3) - Triangle
#joystick.get_button(4) - L1
#joystick.get_button(5) - R1
#joystick.get_button(6) - L2
#joystick.get_button(7) - R2

# Initializes Pygame & sets screen size (Width x Height)
pygame.init()
screen = pygame.display.set_mode((256, 275), 0, 32)
pygame.display.set_caption("BB8 Drive")

pygame.joystick.init()
pygame.joystick.Joystick(1).init()


bb8.set_rgb_led(0, 0, 0, 0, False)

bb8.set_rotation_rate(1, False)

clock = pygame.time.Clock()


def clamp(value, minValue, maxValue):
        if value > maxValue:
                return maxValue
        elif value < minValue:
                return minValue
        else:
                return value

def extra (speed, heading):
    # R1 is pressed bb8 turns around
        if joystick.get_button(5) == 1:
                bb8.set_heading(180, False)
                return    
    # R2 is pressed bb8 sets new heading     
        elif joystick.get_button(7) == 1: 
              # bb8.set_stablization(1, False)
                bb8.set_heading(heading, False)         
                return

       else:
	        sendRollCommand(speed, heading)
                return
          
def mapRange(value, inMin, inMax, outMin, outMax):
        return (value - inMin) * (outMax - outMin) / (inMax - inMin) + outMin

def sendRollCommand(speed, heading):
        lastHeading = 0
        if heading > 0:
                lastHeading = heading

        if speed > 0:
    # L2 Boost
                if joystick.get_button(6) == 1:
                        bb8.boost(50,lastHeading,False)
                        bb8.set_back_led(150, False)
                        return
                else:
                        bb8.roll(speed, lastHeading, 1, False)
                        bb8.set_back_led(150, False)
                        return
        else:
                bb8.roll(0, lastHeading, 0, False)
                return

def draw_axis(surface, x, y, axis_x1, axis_y1, size):
        line_col = (128, 128, 128)
        num_lines = 40
        step = size / float(num_lines)
        joystickCenterX = 128
        joystickCenterY = 128
    

    # Draws grid
        for n in range(num_lines):
                line_col = [(64, 64, 64), (89, 89, 89)][n & 1]
                pygame.draw.line(surface, line_col, (x + n * step, y), (x + n * step, y + size))
                pygame.draw.line(surface, line_col, (x, y + n * step), (x + size, y + n * step))

        pygame.draw.line(surface, (200, 200, 200), (x, y + size / 2), (x + size, y + size / 2))
        pygame.draw.line(surface, (200, 200, 200), (x + size / 2, y), (x + size / 2, y + size))

    # Constrains analog stick input into X & Y coordinates of screen size
        draw_x = int(x + (axis_x1 * size + size) / 2.)
        draw_y = int(y + (axis_y1 * size + size) / 2.)
     

    # Scales x_length & y_length to make sure coordinates are polar instead of elliptical
        x_length = draw_x - joystickCenterX
        y_length = joystickCenterY - draw_y

        if joystickCenterX > joystickCenterY:
                x_length *= joystickCenterY / joystickCenterX
        elif joystickCenterX < joystickCenterY:
                y_length *= joystickCenterX / joystickCenterY

    # Calculates joystick position distance from center
        if joystickCenterX > 0.0 and joystickCenterY > 0.0:
                joystickDistanceFromCenter = math.sqrt(x_length * x_length + y_length * y_length) / min(joystickCenterX, joystickCenterY)
                joystickDistanceFromCenter = clamp(joystickDistanceFromCenter, 0.0, 1.0)
        else:
                joystickDistanceFromCenter = 0.0

    # Calculate the angle
        joystickAngleDegrees = math.atan2(x_length, y_length)

    # Adjust for range between 0 and 2
        if joystickAngleDegrees < 0.0:
                joystickAngleDegrees += 2.0 * math.pi

    # Convert to degrees
        joystickAngleDegrees *= 180.0 / math.pi

        speed = int(mapRange(joystickDistanceFromCenter, 0.0, 1.0, 0, 255))
        heading = int(joystickAngleDegrees)

        message = "X: {}  Y: {} Speed: {} Heading: {}".format(draw_x, draw_y, speed, heading)
        font = pygame.font.SysFont("arial", 15);
        text_surface = font.render(message, True, (255, 153, 0))
        screen.blit(text_surface, (1, 260))
    

    # Calculates joystick indicator and vector line
        draw_pos = (draw_x, draw_y)
        center_pos = (x + size / 2, y + size / 2)

    # Draws joystick indicator and vector line
        pygame.draw.line(surface, (114, 153, 0), center_pos, draw_pos, 2)
        pygame.draw.circle(surface, (134, 179, 0), draw_pos, 10)
     
    
#    print(speed, heading)
        return speed, heading


while True:
        clock.tick(10)

        joystick = pygame.joystick.Joystick(1)

        for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()

        if event.type == KEYDOWN:
                if event.key >= K_0 and event.key <= K_1:
                    num = event.key - K_0


    # axis_size = min(256, 640 / (joystick.get_numaxes()/2))
        axis_size = min(256, 256)

    # pygame.draw.rect(screen, (255, 255, 255), (0, 0, 256, 275))
        pygame.draw.rect(screen, (38, 38, 38), (0, 0, 256, 275))

    # Draw all the axes (analog sticks)
        x = 0
        axis_x1 = joystick.get_axis(0)
        axis_y1 = joystick.get_axis(1)

    # Smooth out the joystick 
        if (abs(axis_x1) < 0.05):
                axis_x1=0
        if (abs(axis_y1) < 0.05):
                axis_y1=0

        if (axis_x1 > 0):
                axis_x1 = math.pow(axis_x1, 2)
        else:
                axis_x1 = -math.pow(-axis_x1, 2)
          
        if (axis_y1 > 0):
                axis_y1 = math.pow(axis_y1, 2)
        else:
                axis_y1 = -math.pow(-axis_y1, 2)

    #   print(axis_x1, axis_y1)   
    # L1 is pressed back light is on
        if joystick.get_button(4) == 1:
                response = bb8.set_back_led(255, True)
                print(response)

        speed, heading = draw_axis(screen, x, 0, axis_x1, axis_y1, axis_size)
        
        extra(heading, speed)
     
        x += axis_size  
        pygame.display.update()
