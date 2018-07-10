'''
    File name: mazer.py
    Author: Fernando Passos, Gildásio Junio, Felipe Regino
    Date created: 09/07/2018
    Date last modified: 10/07/2018
    Python Version: 3.6.5
'''

import sys
import pygame
import math
import random
from cell import Cell

if len(sys.argv) < 4:
    print("Usage: python mazer.py [SCREEN SIZE] [CELL SIZE] [EXECUTION SPEED] ")
    print("After Maze Generation Press Any Key To Start Solving")
    sys.exit()

#Create the generator GUI
pygame.init()
size = (int(sys.argv[1]),int(sys.argv[1]))
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Mazer")
clock = pygame.time.Clock()


#Set the size of cells and the number of cells in each column/row 
cell_size = int(sys.argv[2])
grid = []
cols = math.floor(size[0]/cell_size)
rows = math.floor(size[1]/cell_size)


#Create a cell object for each cell in the maze
for i in range(rows):
    grid.append([])
    for j in range (cols + 1):
        cell = Cell(i, j, cell_size)
        grid[i].append(cell)


#Set used colors
black = pygame.Color(0,0,0)
grey = pygame.Color(105, 105, 105)
white = pygame.Color(255,255,255)
yellow = pygame.Color(240,230,140)
green = pygame.Color(0,150,0)
blue = pygame.Color(0, 0, 200)
red = pygame.Color(150,0, 0)


#Makes the computation for generating the maze
def compute_generation():
    neighbors = []
    current.set_visited()
    i, j = current.get_position()
    #Identify the neighbors of the current cell
    if i > 0:
        top_neighbor = grid[i - 1][j]
    else:
        top_neighbor = None
    if j > 0:
        right_neighbor = grid[i][j - 1]
    else:
        right_neighbor = None
    if i < rows - 1:
        bottom_neighbor = grid[i + 1][j]
    else:
        bottom_neighbor = None
    if j < cols - 1 :
        left_neighbor = grid[i][j + 1]
    else:
        left_neighbor = None    
    #Push the non-visited neighbors to the stack
    if  top_neighbor != None and (not top_neighbor.was_visited()):
        neighbors.append(top_neighbor)
    if  right_neighbor != None and (not right_neighbor.was_visited()):
        neighbors.append(right_neighbor)
    if  bottom_neighbor != None and (not bottom_neighbor.was_visited()):
        neighbors.append(bottom_neighbor)
    if  left_neighbor != None and (not left_neighbor.was_visited()):
        neighbors.append(left_neighbor)      
    #Choose a random neighbor to be visited next
    if len(neighbors) > 0:
        r = random.randint(0, len(neighbors) - 1)
        return neighbors[r]
    else:
        return None
      

#Draw the cells on the GUI
def draw_generation():
    screen.fill(grey)
    for i in range(rows):
        for j in range(cols):
            #Get cell screen cordinates and the situation of it's borders
            x, y = grid[i][j].get_cell_coordinates()
            borders = grid[i][j].get_cell_borders()
            #If the cell is a starter cell it is painted blue
            if grid[i][j].is_starter():
                pygame.draw.rect(screen, blue, (x + 1, y + 1, cell_size, cell_size))
            #If the cell is an exit_cell it is painted green
            elif grid[i][j].is_exit():
                pygame.draw.rect(screen, green, (x + 1, y + 1, cell_size, cell_size))
            #If the cell is being visited it is painted yellos
            elif grid[i][j].is_being_visited():
                pygame.draw.rect(screen, yellow, (x + 1, y + 1, cell_size, cell_size))
            #if the current cell is in a path that leads to a dead end it's painted grey again
            elif grid[i][j].leads_to_dead_end():
                pygame.draw.rect(screen, grey, (x + 1, y + 1, cell_size, cell_size))
            #If the cell was already visited it's painted purple
            elif grid[i][j].was_visited():
                pygame.draw.rect(screen, white, (x + 1, y + 1, cell_size, cell_size))
            #Draw Top Border
            if borders['top']:
                pygame.draw.line(screen, black, (x, y), (x + cell_size, y), 2)
            #Draw Right Border
            if borders['right']:
                pygame.draw.line(screen, black, (x, y + cell_size), (x , y), 2)               
            #Draw Bottom Border
            if borders['bottom']:
                pygame.draw.line(screen, black, (x , y + cell_size), (x + cell_size , y + cell_size),2)
            #Draw Left Border
            if borders['left']:
                pygame.draw.line(screen, black, (x + cell_size, y), (x + cell_size, y + cell_size), 2)
    #Update screen
    pygame.display.flip()


#Remove the borders between the current cell and the chosen cell
def remove_borders():
    current_y, current_x = current.get_position()
    next_y, next_x = chosen.get_position()
    if(current_x - next_x == 1):
        chosen.remove_border('left')
        current.remove_border('right')        
    elif(current_x - next_x == -1):
        current.remove_border('left')
        chosen.remove_border('right')    
    if(current_y - next_y == 1):
        current.remove_border('top')
        chosen.remove_border('bottom')
    elif(current_y - next_y == -1):
        chosen.remove_border('top')
        current.remove_border('bottom')

#Randomly choose one of the maze's dead-ends to be the maze exit
def set_maze_exit():
    dead_ends = []
    for i in range(rows):
        for j in range(cols):
            if grid[i][j].is_dead_end() and not grid[i][j].is_starter():
                dead_ends.append(grid[i][j])
    exit_cell_index = random.randint(0, len(dead_ends) - 1)
    dead_ends[exit_cell_index].set_exit()


#Initialize the generation algorithm by creating a cell stack, picking a random starter cell, and drawing the initial objects to the screen
cell_stack = []
initial_row = random.randint(0, rows - 1)
initial_col = random.randint(0, cols - 1)
current = grid[initial_row][initial_col]
current.set_starter()
current.set_on_visit()
generating = True
draw_generation()
#Execution Loop
while generating:
    #Checks if the program window was closed
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            generating = False
            pygame.quit()
    #Set the framerate of the execution
    clock.tick(int(sys.argv[3]))
    #Pick up a neighbor of the current cell to merge them
    chosen = compute_generation()
    #Check if it was possible to pick a unvisited neighbor of the current cell
    if chosen != None:
        remove_borders()
        cell_stack.append(current)
        current.set_not_on_visit()
        current = chosen
        current.set_on_visit()
    else:
        #If the cell_stack is empty then all nodes have been integrated to the maze and the maze is complete
        if(len(cell_stack) == 0):
            set_maze_exit()
            draw_generation()
            pygame.image.save(screen, 'Maze.jpeg')
            generating = False
            waiting = True
        #If the stack isn't empty and there were no avaliable neighbors then pick the most recent from the stack
        else:
            current.set_not_on_visit()
            current = cell_stack.pop()
            current.set_on_visit()
    draw_generation()


#Wait for a press of a keyboard button to start solving the maze
while(waiting):
    #Checks if the program window was closed
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            waiting = False
            pygame.quit()
        else:
            if i.type == pygame.KEYDOWN:
                waiting = False
                solving = True


#Makes the computation for solving the maze
def solver():
    unvisited_neighbors = []
    current.set_visited()
    i, j = current.get_position()
    borders = current.get_cell_borders()
    #Get a candidate neighbor from all the possible directions if there is one
    if i > 0:
        top_neighbor = grid[i - 1][j]
    else:
        top_neighbor = None
    if j > 0:
        right_neighbor = grid[i][j - 1]
    else:
        right_neighbor = None
    if i < rows - 1:
        bottom_neighbor = grid[i + 1][j]
    else:
        bottom_neighbor = None
    if j < cols - 1 :
        left_neighbor = grid[i][j + 1]
    else:
        left_neighbor = None
    #Check the borders to see if there is an unvisited neighbor among the candidates and if there is add the neighbor to the nighbors list
    if  top_neighbor is not None and (not top_neighbor.was_visited()) and not borders['top']:
        unvisited_neighbors.append(top_neighbor)
    if  right_neighbor is not None and (not right_neighbor.was_visited()) and not borders['right']:
        unvisited_neighbors.append(right_neighbor)
    if  bottom_neighbor is not None and (not bottom_neighbor.was_visited()) and not borders['bottom']:
        unvisited_neighbors.append(bottom_neighbor)
    if  left_neighbor is not None and (not left_neighbor.was_visited()) and not borders['left']:
        unvisited_neighbors.append(left_neighbor)

    if current.is_dead_end() and not current.is_exit():
        current.set_leads_to_dead_end()       

    #If it was possible to find one or more unvisited neighbors, choose randomly one out of the list to be the sucessor     
    if len(unvisited_neighbors) > 0:
        r = random.randint(0, len(unvisited_neighbors) - 1)
        return unvisited_neighbors[r]
    else:
        return None

#Mark all cells as unvisited again
for i in range(rows):
        for j in range(cols):
            grid[i][j].set_not_visited()


#Check if all the the neighbors of the chosen cell were already visited
def check_all_neighbors_visited():
    unvisited_neighbors = []
    borders = chosen.get_cell_borders()
    i, j = chosen.get_position()
    if i > 0:
        top_neighbor = grid[i - 1][j]
    else:
        top_neighbor = None
    if j > 0:
        right_neighbor = grid[i][j - 1]
    else:
        right_neighbor = None
    if i < rows - 1:
        bottom_neighbor = grid[i + 1][j]
    else:
        bottom_neighbor = None
    if j < cols - 1 :
        left_neighbor = grid[i][j + 1]
    else:
        left_neighbor = None
    if  top_neighbor is not None and (not top_neighbor.was_visited()) and not borders['top']:
        unvisited_neighbors.append(top_neighbor)
    if  right_neighbor is not None and (not right_neighbor.was_visited()) and not borders['right']:
        unvisited_neighbors.append(right_neighbor)
    if  bottom_neighbor is not None and (not bottom_neighbor.was_visited()) and not borders['bottom']:
        unvisited_neighbors.append(bottom_neighbor)
    if  left_neighbor is not None and (not left_neighbor.was_visited()) and not borders['left']:
        unvisited_neighbors.append(left_neighbor)

    if len(unvisited_neighbors) == 0:
        return True
    return False
   
#DEBUG
#for i in range(rows):
#    print(grid[i][cols - 2].get_cell_borders())
#print()
#for i in range(rows):
#   print(grid[i][cols - 1].get_cell_borders())
#print()
#for i in range(rows):
#   print(grid[i][0].get_cell_borders())

#Pick the starting cell as the current cell 
current = grid[initial_row][initial_col]
current.set_on_visit()
draw_generation()
while(solving):
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            solving = False
            pygame.quit()
    #Set the framerate of the execution
    clock.tick(int(sys.argv[3]))
    #Pick up a neighbor of the current cell to be the next to be visited
    chosen = solver()
    #Check if it was possible to pick an unvisited neighbor of the current cell
    if chosen != None:
        cell_stack.append(current)
        current.set_not_on_visit()
        current = chosen
        current.set_on_visit()
        #Check if the next neighbor is the exit if it is, the maze is solved
        if chosen.is_exit():
            solving = False
            waiting_to_quit = True
    #If it wasn't possible, pop the most recent cell from the stack
    else:
        current.set_not_on_visit()
        chosen = cell_stack.pop()
        #If the last visited cell(the son of the current cell in the "tree") is a dead-end and all the other neighbors were already visited
        #Then there is no avaliable path from this cell to the exit on this path
        if current.leads_to_dead_end() and check_all_neighbors_visited():
            chosen.set_leads_to_dead_end()
        current = chosen
        current.set_on_visit()
    draw_generation()

#Avoiding the window to close on it's own after solving the maze
while(waiting_to_quit):
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            waiting_to_quit = False
            pygame.quit()