import turtle

def draw_spiral():
    """
    Draw a colorful spiral using the turtle graphics.
    """
    # Set up the screen
    screen = turtle.Screen()
    screen.bgcolor("black")

    # Create a turtle
    t = turtle.Turtle()
    t.speed(0)  # Fastest speed
    t.width(2)

    # Set up colors
    colors = ['red', 'purple', 'blue', 'green', 'orange', 'yellow']

    # Draw the spiral
    for x in range(360):
        t.pencolor(colors[x % 6])  # Cycle through the colors
        t.forward(x)
        t.left(59)  # Rotate the turtle to the left by 59 degrees

    # Close the turtle graphics window
    turtle.done()

if __name__ == "__main__":
    draw_spiral()
