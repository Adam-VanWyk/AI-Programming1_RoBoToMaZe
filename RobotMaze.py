## In this cell, we import all the libraries we are going to use for this notebook
## I recommend you adopt this good-programming practise where all necessary
## libraries for your script are imported and found at the top of the script.
# Make sure you can run this cell with no issues.
# That means, your system should have and support all the necessary libraries.

import pygame
from pygame.locals import *
import sys
import numpy as np
#from numpy import random
import random

def make_game_basics(res, game_title):

    res = res
    screen = pygame.display.set_mode(res)

    pygame.display.set_caption(game_title)

    colors = {"white" :(255,255,255), "black" : (0,0,0),
              "gray" :(100,100,100), "yellow" : (168, 135, 50), "red": (229, 27, 27),
              "blue" : (33, 27, 229), "pink": (242, 192, 227)}

    width = screen.get_width()
    height = screen.get_height()

    return res, screen, colors, width, height

def make_text(myfont, text, color):
  some_text = myfont.render(text, True, color)
  return some_text, some_text.get_size()

    # Finish the function

def make_rect_with_text(surface, color, c1, c2, w, h, text, text_c1, text_c2):
  pygame.draw.rect(surface, color,(c1, c2, w,h))
  surface.blit(text, (text_c1, text_c2))
  return

    # Finish the function

def gridCoords(cellSize, width, height):

    cells_coords = [] 
    for x in range(0, width, cellSize):
        for y in range(0, height-90, cellSize):
            cells_coords.append((x,y))

    return(cells_coords)

def drawGrid(surface, color, cells_coords, cellSize):

    rects_coords = []
    for item in cells_coords:
        pygame.draw.rect(surface, color, (item[0], item[1], cellSize, cellSize), 1) # added 1 to draw only outline
        rects_coords.append((item[0], item[1], cellSize, cellSize))
        # Finish the code

    return(rects_coords)

def drawRobot(surface, color, robot_coords, cellSize):
  pygame.draw.circle(surface, color, (robot_coords[0]+cellSize//2, robot_coords[1]+cellSize//2), cellSize//2)
  return robot_coords

    # Finish the function

def drawGoal(surface, color, goal_coords, cellSize):
  pygame.draw.rect(surface, color, (goal_coords[0], goal_coords[1], cellSize, cellSize))
  return goal_coords

    # Finish the function

def drawObstacles(surface, color, obstacle_coords, cellSize):
  for i in obstacle_coords:
    pygame.draw.rect(surface, color, (i[0], i[1], cellSize, cellSize))
  return obstacle_coords
    # Finish the function

def sample_cells(cells, number=1):

    cells_copy = cells.copy()
    robot_cell = (75, 300)
    goal_cell = (600,300)
    cells_copy.remove(robot_cell)
    cells_copy.remove(goal_cell)

    return robot_cell, goal_cell, random.sample(cells_copy, number)


def legalMove(robot, clicked, rect_coords, obstacles, width, height, cellSize):

    ''' Are we trying to move the robot within the legal limits?
    robot : current position of our robot : coordinates of the corresponding cell
    clicked : coordinates of the cell we have clicked
    rect_coords : the coordinates of the cells in the grid
    obstacles : the coordinates of the cells in the grid that correspond to obstacles
    width : the width of the game window
    height : the height of the game window
    cellSize : the size of each cell

    Function should return updated new_robot_x, new_robot_y coordinates, if the robot can move.
    If not, then the robot should stay where it is (same coordinates)
    '''
    new_robot_x, new_robot_y = robot

    x,y = clicked

    # if the click is within the legal grid area
    if 0 < x < width and 0 < y < height-90:

        cell_x = (x // cellSize) * cellSize
        cell_y = (y // cellSize) * cellSize
        target = (cell_x, cell_y)
        if target not in rect_coords:
            return new_robot_x, new_robot_y
        neighbours = get_valid_neighbours(robot, rect_coords, cellSize, obstacles)
        if target in neighbours:
            new_robot_x , new_robot_y = target
            return new_robot_x, new_robot_y
        
    return new_robot_x, new_robot_y # returns current position if all else fails

def reachedGoal(goal, current):
    ''' Have we reached the goal cell?
    path : history of cells we have clicked to get to the goal
    clicked : coordinates of the cell we have clicked
    goal : the coordinates of the goal cell
    width : the width of the game window
    height : the height of the game window
    cellSize : the size of each cell

    Function should return an activated flag if we have reached the goal cell
    '''
    flag = False
    if current == goal:
        flag = True
        print("Fantastic!")
    return flag

def get_valid_neighbours(current_cell, all_cells, cellSize, obstacles):
    ''' Who are my legal neighbours to which I can move to?
    current_cell : the current cell of the robot : its coordinates
    all_cells : coordinates of all the cells in the grid
    cellSize : the size of each cell
    obstacles: the coordinates of the cells that are obstacles

    Function should return a list that contains the coordinates of the legal neighbours
    '''

    x,y = current_cell
    neighbours = []
    for cell in all_cells:
        if abs(cell[0] - x) + abs(cell[1] - y) == cellSize:
            if cell not in obstacles:
                neighbours.append(cell)

    # Finish the function

    return neighbours

pygame.init()
pygame.font.init()
clock = pygame.time.Clock()

# Task 5.1 [2 Point]: define the resolution of the game and its title, as well the available colors for the game and the width and height
# of the game window, by calling appropriately the make_game_basics function
# The game has been designed for resolution (900, 800)
res, screen, colors, width, height = make_game_basics((900, 800), "RoBoToMaZe")

# Task 5.2 [4 Points]: We have defined a smallfont using the pygame.font.SysFont() syntax below.
# Define a smaller and a bigger font (tinyfont, bigfont)
# Feel free to add more fonts in your game

smallfont = pygame.font.SysFont('Corbel',35)
tinyfont = pygame.font.SysFont('Corbel',15)
bigfont = pygame.font.SysFont('Corbel',50)

# Task 5.3 [3 Points]: We need to create 3 text objects in our game.
# One for the Quit Game button, one for the New Game button and one that
# prints a congratulatory message whenever a player solves the puzzle.
# Using the make_text function, create these three objects.
quit_game = make_text(smallfont, "Quit game.", 'black')
new_game = make_text(smallfont, "New game.", 'black')
win_game = make_text(bigfont, "Fantastic!", 'black')

# Here we decide where do we want our quit game and new game buttons to be and how large we want them to be
# The numbers given are for the tested implementation, the one in the attached picture.

quit_button_coords = [0, 750, 150, 40]
new_game_button_coords = [150, 750, 150, 40]

# Initializing the size of each grid cell
cellSize = 75

def bfs(robot, goal, obstacles, grid_coords):
    visited = {robot}   
    queue = [robot]
    parent = {robot: None} # records path to back-track

    while queue:
        current = queue.pop(0)
        # Check if goal state is reached
        if (current[0] == goal[0] and current[1] == goal[1]):
                break
        
        for neighbor in get_valid_neighbours(current, grid_coords, cellSize, obstacles):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)

    if goal not in parent:
        return None # Goal not reached
        
    path = []
    node = goal        
    while node is not None:
        path.append(node)
        node = parent[node]
    path.reverse()

    return path

def main():

    reached_goal_flag = False

    # Task 5.4 : We need to now draw the cells of our grid.
    # Produce the coordinates for the cells [2 Points]
    # Initialize the robot starting cell, the goal cell and the obstacle cells [3 Points]
    # Start with number = 10 obstacle cells in the sample_cells function

    grid_coords = gridCoords(cellSize, width, height)
    robot_coords, goal_coords, obstacle_coords = sample_cells(grid_coords, 10)

    #all_coords =

    # here make a copy of the coordinates structure that will always contain all cells coordinates
    # in this line, here initialize the robot, goal and obstacle cells

    # path contains the sequence of the cells that we click on while playing the game
    path = []
    path.append((75, 300))

    bfs_path = bfs(robot_coords, goal_coords, obstacle_coords, grid_coords)
    print(bfs_path)
    print(path_cost(bfs_path))

    while True:

        # Inside this while loop is all that happens that we see on the screen : the window, the objects etc. This runs constantly,
        # many times a minute, and by using the Clock, we can reduce that frequency, saving up CPU usage.

        # We create a screen with just white color : this is our canvas
        # feel free to change the background color
        screen.fill(colors["white"])

        # We define as mouse to be where the position of the mouse is at all times (when clicked)
        mouse = pygame.mouse.get_pos()

        # Task 5.5 [5 Points]: Use the draw functions to draw the various cells of the game.
        # You need to first draw the grid. After that you can draw the special cells (robot, goal and obstacles)

        drawGrid(screen, colors["gray"], grid_coords, cellSize)
        drawRobot(screen, colors["red"], robot_coords, cellSize)
        drawGoal(screen, colors["yellow"], goal_coords, cellSize)
        drawObstacles(screen, colors["blue"], obstacle_coords, cellSize)

        quit_game_size = (quit_button_coords[2], quit_button_coords[3])
        new_game_size = (new_game_button_coords[2], new_game_button_coords[3])
        win_game_size = (150, 40)

        # Here we use the make_rect_with_text function to create the quit game button
        make_rect_with_text(screen, colors["gray"], quit_button_coords[0],
                        quit_button_coords[1], quit_button_coords[2],
                        quit_button_coords[3],
                        quit_game[0], quit_button_coords[0]+(quit_game_size[0]/2)-50,
                       quit_button_coords[1] + (quit_game_size[1]/2)-5)

        # Task 5.6 [4 Points]: Following the example above, use the make_rect_with_text function to create the new game button
        make_rect_with_text(screen, colors['gray'], new_game_button_coords[0], new_game_button_coords[1],
                            new_game_button_coords[2], new_game_button_coords[3], new_game[0],
                            new_game_button_coords[0]+(new_game_size[0]/2)-50,
                            new_game_button_coords[1] + (new_game_size[1]/2)-5)


        # The next for loop is found in the pygame scripts, it checks for events that happen and what actions need to happen in case
        # an event occurs
        for ev in pygame.event.get():

            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


            #checks if a mouse is clicked
            if ev.type == pygame.MOUSEBUTTONDOWN:

                if quit_button_coords[0] <= mouse[0] <= quit_button_coords[0]+200 and quit_button_coords[1] <= mouse[1] <= quit_button_coords[1]+50:
                    pygame.quit()
                    sys.exit()

                if new_game_button_coords[0] <= mouse[0] <= new_game_button_coords[0]+200 and new_game_button_coords[1] <= mouse[1] <= new_game_button_coords[1]+50:
                    return main()

                # if the mouse clicks on a cell, then we need to see, is it a free legal cell? and therefore move the robot there

                # Task 5.7 [7 Points]: Using the legalMove function, get the next position of the robot (assuming the click is legal)
                # and update the path list. Then, using the reachedGoal function, check if the robot has reached the goal
                # and if so, activate the corresponding flag

                robot_coords = legalMove((robot_coords), (mouse), grid_coords, obstacle_coords, width, height, cellSize)
                path.append(robot_coords)
                if reachedGoal(goal_coords, robot_coords):
                    reached_goal_flag = True

        # if the flag is true, it means we reached the goal and the congratulatory message should appear
        if reached_goal_flag == True:
            make_rect_with_text(screen, colors["gray"], 150-win_game_size[0]/2, 120-win_game_size[1]/2, win_game_size[0], win_game_size[1]+60,
                        win_game[0], 150-(win_game_size[0]/2),
                       120 + (win_game_size[1]/2))

        # There always need to be a display update, so that, while the game runs, the objects that we wish appear on our screen
        pygame.display.update()
        clock.tick(60)

# Run the game by calling the main function

def manhattanD(cell_a, cell_b, cellSize):
    x1, y1 = cell_a
    x2, y2 = cell_b
    m_distance = (abs(x1 - x2) + abs(y1 - y2)) // cellSize
    return m_distance

def get_bfs_path(robot, goal, obstacles, grid_coords):
   return bfs(robot, goal, obstacles, grid_coords)

def path_cost(path):
    return(len(path))

def euclideanDistance(current_cell, all_cells, goal_cell, cellSize, obstacles):
    ''' Compute the Euclidean distance between every legal next cell and the goal cell.
    Since this is meant to act as a heuristic (estimation of the actual distance), obstacles are not
    taken into consideration as "obstacles".
    current_cell : the coordinates of the current location of the robot
    all_cells : the coordinates of all the cells in the grid
    goal_cell : the coordinates of the target cell
    cellSize : the size of a cell in the grid
    obstacles : the coordinates of the cells that are obstacles

    The function should return a dictionary where key,value is cell, distance of cell to goal cell, sorted in ascending order.
    '''
    x, y = current_cell
    xG, yG = goal_cell
    eDistances = {}

    # Finish the function
    # Compute the distance between the current cell and the goal cell
    # Then, compute the distance between every legal neighbour of the current cell and the goal cell
    # Store these in the eDistances dictionary and return it sorted in ascending order of the distances


def manhattanDistance(current_cell, all_cells, goal_cell, cellSize, obstacles):

    ''' Exactly the same as in the euclideanDistance function.
    The only difference is that now you need to compute the Manhattan Distance.
    The rest of the code would be pretty much the same as in the previous function.
    '''
    neighbors = get_valid_neighbours(current_cell, all_cells, cellSize, obstacles)
    candidates = [current_cell] + neighbors
    distances = {}
    for cell in candidates:
        distances[cell] = manhattanD(cell, goal_cell, cellSize)
    sorted_distances = dict(sorted(distances.items(), key=lambda item: item[1]))
    return sorted_distances

def a_star(current_cell):

    # Finish the code

    return f

main()




