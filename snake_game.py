import turtle
import random
import time

# --- Global Game State Variables ---
GAME_STATE = "START" # Possible states: "START", "PLAYING", "PAUSED", "GAME_OVER"
GAME_SPEED = 0.1 # Initial game speed

# --- Setup the screen ---
screen = turtle.Screen()
screen.setup(width=600, height=600)
screen.bgcolor("black")
screen.title("Snake Game (Ultra Advanced)")
screen.tracer(0)  # Turns off screen updates for smoother animation

# --- Game Border ---
border_pen = turtle.Turtle()
border_pen.speed(0)
border_pen.color("gray")
border_pen.penup()
border_pen.setposition(-290, 290) # Top-left corner
border_pen.pendown()
border_pen.pensize(3)
for _ in range(4):
    border_pen.forward(580)
    border_pen.right(90)
border_pen.penup()
border_pen.hideturtle()

# --- Snake head ---
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("lime green") # Vibrant green for the head
head.penup()
head.goto(0, 0)
head.direction = "stop"

# --- Snake Eyes ---
left_eye = turtle.Turtle()
left_eye.speed(0)
left_eye.shape("circle")
left_eye.color("black") # Black eyes
left_eye.shapesize(stretch_wid=0.4, stretch_len=0.4) # Small eyes
left_eye.penup()

right_eye = turtle.Turtle()
right_eye.speed(0)
right_eye.shape("circle")
right_eye.color("black")
right_eye.shapesize(stretch_wid=0.4, stretch_len=0.4)
right_eye.penup()

# --- Food ---
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("red")
food.penup()
food.goto(0, 100)
food_blink_state = 0 # For food animation

segments = []
score = 0
high_score = 0

# --- Scoreboard ---
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Score: 0  High Score: 0", align="center", font=("Courier", 24, "normal"))

# --- Game Messages Pen (for Start, Pause, Game Over) ---
message_pen = turtle.Turtle()
message_pen.speed(0)
message_pen.color("white")
message_pen.penup()
message_pen.hideturtle()
message_pen.goto(0, 0)


# --- Functions for snake movement ---
def go_up():
    global GAME_STATE
    if GAME_STATE == "PLAYING" and head.direction != "down":
        head.direction = "up"

def go_down():
    global GAME_STATE
    if GAME_STATE == "PLAYING" and head.direction != "up":
        head.direction = "down"

def go_left():
    global GAME_STATE
    if GAME_STATE == "PLAYING" and head.direction != "right":
        head.direction = "left"

def go_right():
    global GAME_STATE
    if GAME_STATE == "PLAYING" and head.direction != "left":
        head.direction = "right"

def toggle_pause():
    """Toggles the game state between PLAYING and PAUSED."""
    global GAME_STATE
    if GAME_STATE == "PLAYING":
        GAME_STATE = "PAUSED"
        message_pen.clear()
        message_pen.write("PAUSED", align="center", font=("Courier", 40, "bold"))
    elif GAME_STATE == "PAUSED":
        message_pen.clear()
        GAME_STATE = "PLAYING"

def start_game():
    """Starts the game from the START or GAME_OVER state."""
    global GAME_STATE, score, high_score, GAME_SPEED
    if GAME_STATE == "START" or GAME_STATE == "GAME_OVER":
        message_pen.clear()
        reset_game_state() # Reset all game elements
        GAME_STATE = "PLAYING"
        GAME_SPEED = 0.1 # Reset speed

def reset_game_state():
    """Resets all game elements to their initial state."""
    global score, high_score, GAME_SPEED
    head.goto(0, 0)
    head.direction = "stop"
    # Reset eye positions
    left_eye.goto(head.xcor() - 5, head.ycor() + 5)
    right_eye.goto(head.xcor() + 5, head.ycor() + 5)

    # Hide and clear all existing segments
    for segment in segments:
        segment.clear()
        segment.hideturtle()
    segments.clear()

    # Reset score and update display
    score = 0
    pen.clear()
    pen.write(f"Score: {score}  High Score: {high_score}", align="center", font=("Courier", 24, "normal"))
    # Move food to initial position
    food.goto(0, 100)


def move():
    # Only move if game is playing
    if GAME_STATE != "PLAYING":
        return

    # Move the head based on its current direction
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)
        # Position eyes relative to head
        left_eye.goto(head.xcor() - 5, head.ycor() + 5)
        right_eye.goto(head.xcor() + 5, head.ycor() + 5)
    elif head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)
        left_eye.goto(head.xcor() - 5, head.ycor() - 5)
        right_eye.goto(head.xcor() + 5, head.ycor() - 5)
    elif head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)
        left_eye.goto(head.xcor() - 5, head.ycor() + 5)
        right_eye.goto(head.xcor() - 5, head.ycor() - 5)
    elif head.direction == "right":
        x = head.xcor()
        head.setx(x + 20)
        left_eye.goto(head.xcor() + 5, head.ycor() + 5)
        right_eye.goto(head.xcor() + 5, head.ycor() - 5)
    else: # "stop" direction, eyes stay with head
        left_eye.goto(head.xcor() - 5, head.ycor() + 5)
        right_eye.goto(head.xcor() + 5, head.ycor() + 5)


def game_over():
    """Handles the game over state."""
    global GAME_STATE, high_score
    GAME_STATE = "GAME_OVER"
    message_pen.clear()
    message_pen.write("GAME OVER!\nPress 'Space' to Restart", align="center", font=("Courier", 24, "bold"))
    # Hide snake and food for game over screen
    head.hideturtle()
    left_eye.hideturtle()
    right_eye.hideturtle()
    food.hideturtle()
    for segment in segments:
        segment.hideturtle()


# --- Keyboard bindings ---
screen.listen()
screen.onkeypress(go_up, "Up")
screen.onkeypress(go_down, "Down")
screen.onkeypress(go_left, "Left")
screen.onkeypress(go_right, "Right")
screen.onkeypress(toggle_pause, "p") # Pause/Resume with 'p' key
screen.onkeypress(start_game, "space") # Start/Restart with 'space' key

# --- Initial Start Screen ---
message_pen.write("Press 'Space' to Start", align="center", font=("Courier", 24, "bold"))
head.hideturtle()
left_eye.hideturtle()
right_eye.hideturtle()
food.hideturtle()


# --- Main game loop ---
while True:
    screen.update()

    if GAME_STATE == "PLAYING":
        # Show snake and food if hidden
        head.showturtle()
        left_eye.showturtle()
        right_eye.showturtle()
        food.showturtle()
        for segment in segments:
            segment.showturtle()

        # Food blinking animation
        if food_blink_state % 10 == 0: # Change color every 10 frames
            if food.color()[0] == "red":
                food.color("orange")
            else:
                food.color("red")
        food_blink_state += 1


        # Check for collision with screen borders
        if head.xcor() > 280 or head.xcor() < -280 or head.ycor() > 280 or head.ycor() < -280:
            game_over()

        # Check for collision with food
        if head.distance(food) < 20:
            # Move the food to a new random location
            x = random.randint(-280, 280)
            y = random.randint(-280, 280)
            food.goto(x, y)

            # Add a new segment to the snake
            new_segment = turtle.Turtle()
            new_segment.speed(0)
            new_segment.shape("circle")
            new_segment.color("forest green") # Darker green for body segments
            new_segment.shapesize(stretch_wid=0.9, stretch_len=0.9) # Default size for body segments
            new_segment.penup()
            segments.append(new_segment)

            # Increase the score and speed
            score += 10
            GAME_SPEED = max(0.05, GAME_SPEED - 0.005) # Increase speed, but not too fast

            if score > high_score:
                high_score = score
            
            pen.clear()
            pen.write(f"Score: {score}  High Score: {high_score}", align="center", font=("Courier", 24, "normal"))

        # Move the end segments first in reverse order
        for index in range(len(segments) - 1, 0, -1):
            x = segments[index - 1].xcor()
            y = segments[index - 1].ycor()
            segments[index].goto(x, y)
            # Ensure all body segments are the normal size (0.9)
            segments[index].shapesize(stretch_wid=0.9, stretch_len=0.9)

        # Move segment 0 to where the head is (if there are segments)
        if len(segments) > 0:
            x = head.xcor()
            y = head.ycor()
            segments[0].goto(x, y)
            segments[0].shapesize(stretch_wid=0.9, stretch_len=0.9) # Ensure first segment is normal size

            # After all segments have shifted, make the very last segment slightly smaller to act as a tail tip
            segments[len(segments) - 1].shapesize(stretch_wid=0.8, stretch_len=0.8)


        move() # Move the snake's head and eyes

        # Check for head collision with body segments
        for segment in segments:
            if segment.distance(head) < 20:
                game_over()

        time.sleep(GAME_SPEED) # Use dynamic game speed

    elif GAME_STATE == "GAME_OVER":
        # Keep game over screen visible
        pass # No updates needed, just wait for spacebar

    elif GAME_STATE == "START":
        # Keep start screen visible
        pass # No updates needed, just wait for spacebar

    elif GAME_STATE == "PAUSED":
        # Keep paused screen visible
        pass # No updates needed, just wait for 'p' key

screen.mainloop()
