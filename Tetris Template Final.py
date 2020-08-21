
from tetris_classes import *
from random import randint
import pygame

pygame.init()

HEIGHT = 600
WIDTH = 800  # Dimensions of the screen
GRIDSIZE = HEIGHT // 24  # size of grid in proportion to the size of the screen(height)
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# ---------------------------------------#
#   pictures                            #
# ---------------------------------------#

background = pygame.image.load("background.jpg")
background = background.convert_alpha()
background = pygame.transform.scale(background, (800, 600))  # loading and resizing background image
intro = pygame.image.load("intro.jpg")
intro = intro.convert_alpha()  # loading and resizing intro image
gameOver = pygame.image.load("gameOver.jpg")
gameOver = gameOver.convert_alpha()  #
gameOver = pygame.transform.scale(gameOver, (800, 600))  # loading and resizing game over image


###MUSIC####
pygame.mixer.music.load('BackgroundMusic.mp3') ##
pygame.mixer.music.set_volume(0.4)  # https://www.pygame.org/docs/ref/music.html
pygame.mixer.music.play(loops=-1)  #
#ping = pygame.mixer.Sound('THE Boom Sound Effect.mp3')   # https://www.pygame.org/docs/ref/mixer.html
#ping.set_volume(0.8)                    #



# ---------------------------------------#
#   other variables                     #
# ---------------------------------------#

timer = 0  # time played
GRIDCLR = (50, 50, 50)  # colour of grid
score = 0  # score achieved
size = 60  # size used for fonts
font = pygame.font.SysFont("Digital Tech", size)  #
font2 = pygame.font.SysFont("Digital Tech", size * 2)  #
delay = 150  # overall delay (speed) of game
hold = True  # Hold boolean

# ---------------------------------------#
COLUMNS = 14  #
ROWS = 22  #
LEFT = 9  #
RIGHT = LEFT + COLUMNS  #
MIDDLE = LEFT + COLUMNS // 2  #
TOP = 1  #
BOTTOM = TOP + ROWS  #


# ---------------------------------------#

# ---------------------------------------#
#   functions                           #
# ---------------------------------------#
def intro_screen():
    screen.blit(intro, (0, 0))  ## blit intro image
    text6 = font2.render("TETRIS GAME", 1, PINK)  ##
    text7 = font.render("Press the space bar to begin:)", 1, WHITE)  ## texts being printed in intro screen
    screen.blit(text6, (100, 0))  ## blit texts
    screen.blit(text7, (110, 100))  ##

def game_over():
    screen.blit(gameOver, (0, 0))  ## blit game over image
    text8 = font.render("SCORE: " + str(score), 1, YELLOW)
    text9 = font.render("TIME: " + str(int(round(timer, 0))) + " sec", 1,ORANGE)  ## blits texts in game over screen
    screen.blit(text8, (220, 330))
    screen.blit(text9, (230, 380))
    pygame.display.update()

def redraw_screen():
    screen.blit(background, (0, 0))  # blits background image
    draw_grid()  # function which draws grid
    shadow.draw(screen, GRIDSIZE)  # draws shadow
    tetra.draw(screen, GRIDSIZE)  # draws tetra piece
    newTetra.draw(screen, GRIDSIZE)  # draws next shape
    holdPiece.draw(screen, GRIDSIZE)  # draws shape in hold
    obstacle.draw(screen, GRIDSIZE)  # draws obstacles

    text = font.render("score: " + str(score), 1, PINKY)  #
    text2 = font.render("level: " + str(level), 1, PINKY)  #
    text3 = font.render("time: " + str(int(round(timer, 0))), 1, PINKY)  # all texts present in play screen
    text4 = font.render("Hold", 1, PINKY)  #
    text5 = font.render("Next", 1, PINKY)  #

    screen.blit(text, (10, 0))  #
    screen.blit(text2, (620, 0))  #
    screen.blit(text3, (10, 500))  # blits all texts in play screen
    screen.blit(text4, (60, 200))  #
    screen.blit(text5, (650, 200))  #
    pygame.display.update()


def draw_grid():  ## function which draws grid
    """ Draw horisontal and vertical lines on the entire game window.
        Space between the lines is GRIDSIZE.
    """
    for x in range(GRIDSIZE // 24 + 224, WIDTH - 220, GRIDSIZE):  #
        pygame.draw.line(screen, GRIDCLR, (x, 25), (x, HEIGHT - 25), 1)  # draws vertical line segments
    for y in range(GRIDSIZE // 24 + 24, HEIGHT, GRIDSIZE):  #
        pygame.draw.line(screen, GRIDCLR, (225, y), (WIDTH - 225, y), 1)  # draws horizontal line segments


# ---------------------------------------#
#   main program                        #
# ---------------------------------------#

shapeNo = randint(1, 7)  # random shape number spawing first shape
newShapeNo = randint(1, 7)  # random new shape number spawing next shape
holdShapeNo = randint(1, 7)  # random hold shape number spawing held shape
shadow = Shape(MIDDLE, BOTTOM - 1, shapeNo)  # coordinates of shadow
tetra = Shape(MIDDLE, TOP, shapeNo)  # coordinates of tetra being played
bottom = Floor(LEFT, BOTTOM, COLUMNS)  # coordinates of bottom
top = Floor(LEFT, TOP, COLUMNS)  # coordinates of top
leftWall = Wall(LEFT - 1, TOP - 1, ROWS)  # coordinates of leftWall
rightWall = Wall(RIGHT, TOP - 1, ROWS)  # coordinates of rightWall
obstacle = Obstacles(LEFT, BOTTOM)  # coordinates of obstacle
newTetra = Shape(MIDDLE + 11, TOP + 12, newShapeNo)  # coordinates of next shape
holdPiece = Shape(MIDDLE - 13, TOP + 12, holdShapeNo)  # coordinates of hold shape
inPlay = 1  # in play checking if game is at intro, gamefield or gameover screen

while inPlay == 1:  ## intro screen
    intro_screen()

    for event in pygame.event.get():  # check for any events
        keys = pygame.key.get_pressed()
        if event.type == pygame.KEYDOWN:
            if keys[pygame.K_SPACE] or keys[pygame.K_KP_ENTER]:  ## if space or enter is pressed, start game
                inPlay = 2
        if event.type == pygame.QUIT:  ## if x is clicked quit game
            inPlay = 4
        if event.type == pygame.KEYDOWN:  ## if esc is pressed quit game
            if keys[pygame.K_ESCAPE]:
                inPlay = 4

    pygame.display.update()  # display must be updated, in order
    # to show the drawings

while inPlay == 2:  ## gamefield screen

    tetra.move_down()
    shadow.shadow_spawn()  ## spawns shadow using shadow class

    if tetra.collides(bottom) or tetra.collides(obstacle):
        tetra.move_up()
        obstacle.append(tetra)

        fullRows = obstacle.findFullRows(TOP, BOTTOM,
                                         COLUMNS)  # finds the full rows and removes their blocks from the obstacles
        obstacle.removeFullRows(fullRows)
        shapeNo = newShapeNo
        shadow = Shape(MIDDLE, BOTTOM - 1, shapeNo)
        tetra = Shape(MIDDLE, TOP, shapeNo)
        newShapeNo = randint(1, 7)  ##generates new random shape
        newTetra = Shape(MIDDLE + 11, TOP + 12, newShapeNo)
        obstacle.removeFullRows(fullRows)
        hold = True  ## turns hold boolean to true as it spawns new tetra to allow holding

        if len(fullRows) == 1:  ## if one line is cleared score increases by 100
            score += 100
        elif len(fullRows) == 2:  ## if two lines are cleared score increases by 200
            score += 200
        elif len(fullRows) == 3:  ## if three lines are cleared score increases by 300
            score += 300
        elif len(fullRows) == 4 and previousTetris == False:  ## if four lines are cleared score increases by 800
            score += 800
            previousTetris = True
        elif len(fullRows) == 4 and previousTetris == True:  ## if four lines are cleared twice in a row score increases by 1200
            score += 1200
            previousTetris = False

    while not (shadow.collides(bottom) or shadow.collides(obstacle)):  ## shadow moves down when not colliding
        shadow.move_down()
    while shadow.collides(bottom) or shadow.collides(obstacle):  ## shadow moves up once when collides with obstacle
        shadow.move_up()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  ## exit when x is clicked
            inPlay = 4

        keys = pygame.key.get_pressed()
        if event.type == pygame.KEYDOWN:  ## exit when esc is pressed
            if keys[pygame.K_ESCAPE]:
                inPlay = 4
        if event.type == pygame.KEYDOWN:  ## rotate the shape when up arrow is pressed
            if event.key == pygame.K_UP:

                tetra.rotate_clkwise()
                shadow.rotate_shadow(tetra)

                if tetra.collides(leftWall) or tetra.collides(rightWall) or tetra.collides(bottom) or tetra.collides(
                        obstacle):  ## counter rotate if it collides with obstacle
                    tetra.rotate_cntclkwise()
                    shadow.rotate_cntclkwise()

            if event.key == pygame.K_LEFT:
                tetra.move_left()
                shadow.move_left()
                if tetra.collides(leftWall) or tetra.collides(obstacle):
                    tetra.move_right()
                    shadow.move_right()

            if event.key == pygame.K_RIGHT:
                tetra.move_right()
                shadow.move_right()
                if tetra.collides(rightWall) or tetra.collides(obstacle):
                    tetra.move_left()
                    shadow.move_left()

            if event.key == pygame.K_DOWN or event.key == pygame.K_LSHIFT:  ## if shift or down arrow is pressed, current shape goes to held and shape in hold turns to current shape
                if hold == True:
                    (holdShapeNo, shapeNo) = (
                    shapeNo, holdShapeNo)  ## switches current shape with held shape (stores in hold)
                    holdPiece = Shape(MIDDLE - 12, TOP + 12, holdShapeNo)
                    shadow = Shape(MIDDLE, BOTTOM - 1, shapeNo)
                    tetra = Shape(MIDDLE, TOP, shapeNo)
                    hold = False  ## turns hold boolean to false so it can only be done once per tetra

            if event.key == pygame.K_SPACE:  ## when space is pressed, tetris goes all the way down until it hits an obstacle
                while not (tetra.collides(bottom) or tetra.collides(obstacle)):
                    tetra.move_down()
                tetra.move_up()
                obstacle.append(tetra)

                fullRows = obstacle.findFullRows(TOP, BOTTOM,COLUMNS)  # finds the full rows and removes their blocks from the obstacles
                shapeNo = newShapeNo
                shadow = Shape(MIDDLE, BOTTOM - 1, shapeNo)
                tetra = Shape(MIDDLE, TOP, shapeNo)
                newShapeNo = randint(1, 7)  ##generates new random shape
                newTetra = Shape(MIDDLE + 11, TOP + 12, newShapeNo)
                obstacle.removeFullRows(fullRows)
                hold = True  ## turns hold boolean to true as it spawns new tetra to allow holding

                if len(fullRows) == 1:  ## if one line is cleared score increases by 100
                    score += 100
                    delay -= 10  ##  delay is decreased by 10 meaning taht tetra fall faster
                    ping.play()
                elif len(fullRows) == 2:  ## if two lines are cleared score increases by 200
                    score += 200
                    ping.play()
                elif len(fullRows) == 3:  ## if three lines are cleared score increases by 300
                    score += 300
                    ping.play()
                elif len(fullRows) == 4 and previousTetris == False:  ## if four lines are cleared score increases by 800 (tetris)
                    score += 800
                    ping.play()
                    previousTetris = True
                elif len(fullRows) == 4 and previousTetris == True:  ## if four lines are cleared twice in a row score increases by 1200
                    score += 1200
                    ping.play()
                    previousTetris = False


    if obstacle.collides(top):  ## ends game if obstacles reach the top
        inPlay = 3

    redraw_screen()
    pygame.time.delay(delay)  # delay
    timer += 0.001 * delay  # timer

while inPlay == 3:  ## game over screen
    game_over()
    pygame.display.update()

    for event in pygame.event.get():  # check for any events
        keys = pygame.key.get_pressed()
        if event.type == pygame.KEYDOWN:  ## exit if esc is pressed
            if keys[pygame.K_ESCAPE]:
                inPlay = 4
        if event.type == pygame.QUIT:  ## exit if x is clicked
            inPlay = 4
pygame.mixer.music.stop()
pygame.quit()  # always quit pygame when done!