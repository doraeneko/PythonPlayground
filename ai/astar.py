#
# Some fun with A*
#
# June 2019
# (C) Andreas Gaiser

import tkinter
import random
import numpy


class GameArena(object):
    '''Generate a primitive game arena to find paths in'''

    def __init__(self, size_x, size_y, seed, difficulty):
        self._size_x = size_x
        self._size_y = size_y
        self._max_weight = difficulty
        rnd = random.Random(seed)
        self._area = numpy.zeros((size_x, size_y), numpy.float)
        for x in range(0, size_x):
            for y in range(0, size_y):
                self._area[x, y] = rnd.randint(1, self._max_weight) \
                    #(1000.0 if x == y else
                    #                0.0 if rnd.randint(0, difficulty)
                    #                else 1.0 if rnd.randint(0, difficulty) else 1000.0)
        print(self._area)

    def get_color(self, x, y):
        '''Create a color for a single field'''
        return "#%02x%02x%02x" % (32, int(256.0*(1.0 - self._area[x, y] / self._max_weight)), 0)

    def draw(self, window):
        delta = 20
        for x in range(0, self._size_x):
            for y in range(0, self._size_y):
                color = "green" if self._area[x,y] < 1.0 else "brown" if self._area[x,y] < 100.0 else "black"
                w.create_rectangle(x * delta, y * delta, (x + 1) * delta, (y + 1) * delta, fill=self.get_color(x,y))

    def draw_astar(self, windows, the_color, distance_func = None):
        delta = 20
        a_star_path = self.astar((0,0), (self._size_x-1, self._size_y-1), distance_func = distance_func)
        for (x, y) in a_star_path:
            w.create_oval(x * delta+delta/3, y * delta + delta/3, x * delta+2*(delta/3), y * delta + 2*(delta/3), fill=the_color)
        print("A*: %s" % self.astar((0,0), (self._size_x-1, self._size_y-1)))


    def astar(self, start_point, end_point, distance_func = None):

        def manhattan_distance(p1, p2):
            (x1, y1) = p1
            (x2, y2) = p2
            return abs(x1-x2) + abs(y1-y2)

        def get_entry(the_array, point):
            (x, y) = point
            return the_array[x,y]

        def set_entry(the_array, point, value):
            (x, y) = point
            the_array[x, y] = value

        def get_neighbors(point):
            (x, y) = point
            if x > 0:
                yield (x-1, y)
            if x < self._size_x-1:
                yield (x+1, y)
            if y > 0:
                yield (x, y-1)
            if y < self._size_y-1:
                yield (x, y+1)

        if distance_func is None:
            distance_func = manhattan_distance

        closed_elements = set()
        pred = {}

        g_score = numpy.full([self._size_x, self._size_y], 9999999.9)
        f_score = numpy.full([self._size_x, self._size_y], 9999999.9)
        g_score[0, 0] = 0.0
        f_score[0, 0] = 0.0
        open_elements = set([start_point])

        def get_element_with_minimal_f():
            min_value = None
            min_element = None
            for (x, y) in open_elements:
                if min_value is None or f_score[x, y] < min_value:
                    min_value = f_score[x,y]
                    min_element = (x,y)
            return min_element


        while any(open_elements):
            current = get_element_with_minimal_f()
            open_elements.remove(current)

            if current == end_point:
                # construct the path
                path = [current]
                path_element = current
                while path_element in pred:
                    path_element = pred[path_element]
                    path.append(path_element)
                return path

            closed_elements.add(current)
            for neighbor in get_neighbors(current):
                (nx, ny) = neighbor
                if neighbor in closed_elements:
                    continue
                g_candidate = g_score[nx, ny] + self._area[nx, ny]
                if neighbor not in open_elements:
                    open_elements.add(neighbor)
                elif g_candidate >= g_score[nx, ny]:
                    continue

                pred[neighbor] = current
                g_score[nx, ny] = g_candidate
                f_score[nx, ny] = g_score[nx, ny] + distance_func(neighbor, end_point)






        pass

master = tkinter.Tk()

canvas_width = 800
canvas_height = 700
w = tkinter.Canvas(master,
           width=canvas_width,
           height=canvas_height)
w.pack()

g = GameArena(30, 30, 1, 5.00)
g.draw(w)
g.draw_astar(w, "blue") # default heuristic: Manhattan distance
g.draw_astar(w, "red", distance_func=lambda p1, p2: 0.0) # Dijkstra

tkinter.mainloop()