'''
    File name: cell.py
    Author: Fernando Passos, Gildásio Junio, Felipe Regino
    Date created: 09/07/2018
    Date last modified: 09/07/2018
    Python Version: 3.6.5
'''
import pygame


class Cell:
    def __init__(self, position_y, position_x, size):
        self.position_x = position_x
        self.position_y = position_y
        self.size = size
        self.starting_cell = False
        self.exit_cell = False
        self.borders = {
            'top' : True, 
            'right': True, 
            'bottom': True, 
            'left': True
        }
        self.visited = False
        self.on_visit = False
    

    def get_cell_coordinates(self):
        x = self.position_x * self.size
        y = self.position_y * self.size
        return x, y


    def get_cell_borders(self):
        return self.borders


    def set_visited(self):
        self.visited = True


    def was_visited(self):
        return self.visited


    def get_position(self):
        return self.position_y, self.position_x
    

    def remove_border(self, border):
        self.borders[border] = False

    def is_being_visited(self):
        return self.on_visit


    def set_on_visit(self):
        self.on_visit = True


    def set_not_on_visit(self):
        self.on_visit = False

    def is_dead_end(self):
        count = 0
        for side, status in self.borders.items():
            if status:
                count += 1
        if count == 3:
            return True
        else:
            return False

    def set_starter(self):
        self.starting_cell = True

    def is_starter(self):
        return self.starting_cell

    def is_exit(self):
        return self.exit_cell

    def set_exit(self):
        self.exit_cell = True

    def set_not_visited(self):
        self.visited = False