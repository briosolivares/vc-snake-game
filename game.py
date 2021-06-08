from sense_hat import SenseHat
from time import sleep
import random
import voice

sense = SenseHat()
sense.low_light = True

GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
START_DELAY = 3
MATRIX_MIN_VALUE = 0
MATRIX_MAX_VALUE = 7
MATRIX_SIZE = 8

def game():
    ### 1. CREATE LISTENER FOR SPEECH CLASSIFIER
    listener = voice.AudioClassifier(model_file=voice.VOICE_MODEL,
                                    labels_file=voice.VOICE_LABELS,
                                    audio_device_index=2)
    while True:
        gameOverFlag = False
        growSnakeFlag = False
        generateRandomFoodFlag = False
        snakeMovementDelay = 0.5
        snakeMovementDelayDecrease = -0.02
        score = 0

        sense.clear()
        sense.show_message("Welcome to VC Snake Game!")

        # Set default snake starting position
        snakePosX = [3] # x-axis (from left to right) [0,1,2,3,4,5,6,7]
        snakePosY = [5] # y-axis (from top to bottom) [1,2,3,4,5,6,7,8]
    
        # Generate random food position
        while True:
            foodPosX = random.randint(0, 7)
            foodPosY = random.randint(0, 7)
            # If the food position (x,y) does not equal the snake position (x,y),
            # then we are GOOD
            if foodPosX != snakePosX[0] or foodPosY != snakePosY[0]:
                break

        # Set default snake starting direction
        movementX = 0 # Sets the x-direction
        movementY = 1 # Sets the y-direction (-1: goes from bottom to top; 1: goes from top to bottom)

        while not gameOverFlag:
            # Check if snake eats food
            # If snake eats food, we must: grow the snake, generate a new food, 
            # increase the snake speed, and increment the user's score
            if foodPosX == snakePosX[0] and foodPosY == snakePosY[0]:
                growSnakeFlag = True
                generateRandomFoodFlag = True
                snakeMovementDelay += snakeMovementDelayDecrease
                score +=1
            
            # Check if snake bites itself
            for i in range(1, len(snakePosX)):
                if snakePosX[i] == snakePosX[0] and snakePosY[i] == snakePosY[0]:
                    gameOverFlag = True

            # Check if game-over
            if gameOverFlag:
                break

            # Check voice commands
            ### 2. RESPOND TO SPEECH CLASSIFICATIONS
            command = listener.next(block=False)
            if command:
                command = str(command[0])
                if command == "go_left" and movementX != 1:
                    movementX = -1
                    movementY = 0
                elif command == "go_right" and movementX != -1:
                    movementX = 1
                    movementY = 0
                elif command == "go_up" and movementY != 1:
                    movementY = -1
                    movementX = 0
                elif command == "go_down" and movementY != -1:
                    movementY = 1
                    movementX = 0

            # Grow snake
            if growSnakeFlag:
                growSnakeFlag = False
                snakePosX.append(0)
                snakePosY.append(0)

            # Move snake
            for i in range((len(snakePosX) - 1), 0, -1):
                snakePosX[i] = snakePosX[i - 1]
                snakePosY[i] = snakePosY[i - 1]

            snakePosX[0] += movementX
            snakePosY[0] += movementY

            # Check game borders
            if snakePosX[0] > MATRIX_MAX_VALUE:
                snakePosX[0] -= MATRIX_SIZE
            elif snakePosX[0] < MATRIX_MIN_VALUE:
                snakePosX[0] += MATRIX_SIZE
            if snakePosY[0] > MATRIX_MAX_VALUE:
                snakePosY[0] -= MATRIX_SIZE
            elif snakePosY[0] < MATRIX_MIN_VALUE:
                snakePosY[0] += MATRIX_SIZE

            # Spawn random food
            if generateRandomFoodFlag:
                generateRandomFoodFlag = False
                retryFlag = True
                while retryFlag:
                    foodPosX = random.randint(0, 7)
                    foodPosY = random.randint(0, 7)
                    retryFlag = False
                    for x, y in zip(snakePosX, snakePosY):
                        if x == foodPosX and y == foodPosY:
                            retryFlag = True
                            break

            # Update matrix
            sense.clear()
            sense.set_pixel(foodPosX, foodPosY, RED)
            for x, y in zip(snakePosX, snakePosY):
                sense.set_pixel(x, y, GREEN)

            # Snake speed (game loop delay)
            sleep(snakeMovementDelay)

        # Blink the dead snake
        for loop in range (5):
            sense.clear()
            sense.set_pixel(foodPosX, foodPosY, RED)
            for x, y in zip(snakePosX, snakePosY):
                sense.set_pixel(x, y, RED)
            sleep(0.5)
            
            sense.clear()
            sense.set_pixel(foodPosX, foodPosY, RED)
            for x, y in zip(snakePosX, snakePosY):
                sense.set_pixel(x, y, GREEN)
            sleep(0.5)

        sense.clear()

        # Display score
        while score:
            sense.show_message("Score: {}".format(score), text_colour=YELLOW)
            return score