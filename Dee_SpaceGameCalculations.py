import math

# constants
g = 9.8  # gravitational acceleration in m/s^2
MAX_WIDTH = 1200
MAX_HEIGHT = 600

# calculate maximum velocity for given canvas size
def max_velocity(max_width, max_height):
    max_x = max_width
    # launch from the middle of the screen to get max vertical distance
    max_y = max_height / 2  
    # launch angle of 45 degrees for maximum horizontal distance
    v0_x = math.sqrt((max_x * g) / math.sin(2 * angle_rad))
    angle_rad = math.pi / 4  
    v0_y = math.sqrt(2 * g * max_y)
    return max(v0_x, v0_y)

# calculate and print the maximum velocity
max_v = max_velocity(MAX_WIDTH, MAX_HEIGHT)
print(f"The maximum allowable velocity for the given canvas size is {max_v:.2f} m/s.")
