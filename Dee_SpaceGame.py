# NOTE: I added some comments for documentation and explanations. I hope it helps a lot!! — Dee ★
import pygame
import math
import numpy as np
import random

"""
★ MY PROJECT DETAILS: ★

*** Project Proposal: Dee's CiP 2024 Space Simulation Project

*** My Project Description: Dee's CiP 2024 Space Simulation Project is a Python-based simulation that offers users a virtual space mission experience. 
    I encourage users to input the initial velocity and launch angle of a rocket so that the program simulates its trajectory based on physics 
    principles. The simulation includes visual elements such as a starry background, a spaceship that follows the trajectory, and shows 
    additional information about the values of its velocity, launch angle, maximum horizontal distance, and maximum vertical distance.

*** My Project's Key Features:

    1. User Input - users can input the initial velocity (within a defined range) and launch angle (0-90 degrees) of the rocket.
    2. Physics Simulation - the program calculates and displays the rocket's trajectory based on the provided inputs.
    3. Visual Elements - the features a starry background with twinkling stars and a spaceship image that follows the calculated trajectory.
    4. Informative Text - it displays key parameters such as velocity, launch angle, and maximum distances (horizontal and vertical) on the screen
    5. Engaging Experience - the users can explore different combinations of initial velocity and launch angle to see their effects on the rocket's trajectory and maximum distances.

*** My Project's Purpose:

    1. It provides an interactive way for users to learn about physics concepts such as projectile motion and gravitational acceleration.
    2. I think it's a very fun way to use because of the visual elements and interactive nature of the simulation make it engaging for users of all ages.
    3. It allows users to adjust the initial parameters to explore various scenarios to gain a deeper understanding of the underlying physics principles.

*** My Project's Brief Description:

    Dee's CiP 2024 Space Simulation Project is a Python-based simulation that enables users to explore the principles of projectile motion and 
    space exploration in a virtual environment. Users can input the initial velocity and launch angle of a rocket and my program simulates its 
    trajectory through the use of physics principles. It includes visual elements such as a starry background and a spaceship image that follows 
    its calculated trajectory. The informative text at the top-most part displays the key parameters like velocity and maximum distances to 
    provide context to the simulation. My project's purpose is to offer a fun and educational experience for users to experiment with different 
    scenarios by varying the input values and then gain an intuitive understanding of interesting physics concepts!!

"""

# initialize Pygame
pygame.init()

# declare and initialize the constant values
g = 9.8
MAX_WIDTH = 1200 
MAX_HEIGHT = 800
MIN_VELOCITY = 0  
MAX_VELOCITY = 108

# calculate maximum horizontal distance (launch angle in radians)
def max_horizontal_distance(v0, angle):
    angle_rad = np.radians(angle)  
    return (v0 ** 2) * np.sin(2 * angle_rad) / g

# calculate maximum vertical distance (launch angle in radians)
def max_vertical_distance(v0, angle):
    angle_rad = np.radians(angle) 
    return (v0 ** 2) * np.sin(angle_rad) ** 2 / (2 * g)

# prompt user for the velocity and angle input values
while True:
    # try - catch method for invalid inputs
    try:
        # displays the title of my space simulation project
        print(f"★--Dee's Space Simulation Project--★")
        print(f"★--Please enter the required details to proceed--★")
        print(f"---------------------------------------------------")

        # velocity input
        v0 = float(input(f"Enter initial velocity (m/s, limit: {MIN_VELOCITY}-{MAX_VELOCITY}): "))
        if v0 < MIN_VELOCITY or v0 > MAX_VELOCITY:
            raise ValueError(f"Velocity must be between {MIN_VELOCITY} and {MAX_VELOCITY} m/s.")
        
        # angle input
        angle = float(input("Enter launch angle (degrees, limit: 0-90): "))
        if angle <= 0 or angle > 90:
            raise ValueError("Angle must be between 0 and 90 degrees.")

        # calculate maximum distances (horizontal and vertical)
        max_x = max_horizontal_distance(v0, angle)
        max_y = max_vertical_distance(v0, angle)

        # condition for invalid inputs
        if max_x > MAX_WIDTH or max_y > MAX_HEIGHT:
            raise ValueError(f"The trajectory exceeds the maximum displayable range. "
                             f"Maximum horizontal distance: {MAX_WIDTH} pixels, "
                             f"Maximum vertical distance: {MAX_HEIGHT} pixels.")

        break

    except ValueError as e:
        print(e)


# initialize Pygame screen
screen_width, screen_height = MAX_WIDTH, MAX_HEIGHT
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Space Mission Simulator')

# color values
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
STAR_COLOR = (254, 157, 97)

# font style
font = pygame.font.SysFont('monospace', 18)

# calculate trajectory points
trajectory_points = []
# convert launch angle to radians
angle_rad = math.radians(angle)  
t_flight = 2 * v0 * math.sin(angle_rad) / g
t = 0
dt = 0.1

while t < t_flight:
    x = v0 * math.cos(angle_rad) * t
    y = v0 * math.sin(angle_rad) * t - 0.5 * g * t**2
    # flips y-axis for screen coordinates
    trajectory_points.append((x, screen_height - y))  
    t += dt

# generate starry background display
stars = [(random.randint(0, screen_width), random.randint(0, screen_height)) for _ in range(100)]

# load the spaceship png hehehe
spaceship_img = pygame.image.load('Dee_spaceship.png')
spaceship_img = pygame.transform.scale(spaceship_img, (50, 50))
rotated_spaceship = pygame.transform.rotate(spaceship_img, -90)

# main program loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)

    # draw stars
    for star in stars:
        pygame.draw.circle(screen, STAR_COLOR, (star[0], star[1]), 1)

    # generate twinkling stars by randomly changing their alpha value
    if random.random() < 0.01:
        for i, star in enumerate(stars):
            stars[i] = (star[0], star[1], random.randint(100, 255))

    # calculate the position of the spaceship
    midpoint_index = int(len(trajectory_points) / 2)
    # condition -- if the velocity and angle are within specific ranges
    if v0 < MAX_VELOCITY and (angle < 45 or angle > 135):  
        # center the spaceship horizontally and vertically
        spaceship_pos = ((screen_width - rotated_spaceship.get_width()) / 2,
                        (screen_height - rotated_spaceship.get_height()) / 2)
    else:
        # otherwise, calculate the position based on the trajectory
        spaceship_pos = (trajectory_points[midpoint_index][0] - rotated_spaceship.get_width() / 2,
                        trajectory_points[midpoint_index][1] - rotated_spaceship.get_height() / 2)

    screen.blit(rotated_spaceship, spaceship_pos)

    # calculate the offset needed to center the trajectory
    # check if velocity and angle are within specific ranges (less than 45 or greater than 135)
    if v0 < MAX_VELOCITY and (angle < 45 or angle > 135):  
        offset_x = (screen_width - max_x) / 2
    else:
        offset_x = 0

    # draw trajectory
    for point in trajectory_points:
        pygame.draw.circle(screen, YELLOW, (int(point[0] + offset_x), int(point[1])), 2)

    # display additional information (top space, title text at the center, and line spacing)
    # title text
    text_y = 60
    title_text = font.render("Dee's Code In Place 2024 Space Simulation Project", True, WHITE) 
    screen.blit(title_text, ((screen_width - title_text.get_width()) / 2, 20))  
    # increase vertical position for the next text (line spacing)
    text_y += 40  

    # velocity text
    velocity_text = font.render(f"Velocity: {v0} m/s", True, WHITE)
    screen.blit(velocity_text, ((screen_width - velocity_text.get_width()) / 2, text_y))
    # increase vertical position for the next text (line spacing)
    text_y += 30

    # launch angle text
    angle_text = font.render(f"Launch Angle: {angle} degrees", True, WHITE)
    screen.blit(angle_text, ((screen_width - angle_text.get_width()) / 2, text_y))
    # increase vertical position for the next text (line spacing)
    text_y += 30

    # max horizontal distane text
    max_horizontal_text = font.render(f"Max Horizontal Distance: {max_x:.2f} meters", True, WHITE)
    screen.blit(max_horizontal_text, ((screen_width - max_horizontal_text.get_width()) / 2, text_y))
    # increase vertical position for the next text (line spacing)
    text_y += 30

    # max vertical distane text
    max_vertical_text = font.render(f"Max Vertical Distance: {max_y:.2f} meters", True, WHITE)
    screen.blit(max_vertical_text, ((screen_width - max_vertical_text.get_width()) / 2, text_y))

    pygame.display.flip()

pygame.quit()