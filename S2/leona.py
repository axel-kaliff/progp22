from node import Node
import math
import sys


class Leona:
    # Initial positon of Leona

    position = (0,0)
    direction = 0       # In degrees clockwise from straight north
    color = "#0000FF"
    drawing = False     # True if pen is down, False if pen is up



    ### Functions for moving Leona ###


    # Should be called each time Leona moves forward/back && drawing == True
    # Draws a line segment with "color + start x + start y + end x + end y"
    # Write coordinates with at least 4 decimals
    def draw(self, end_position):
        
        to_draw = []
        to_draw.append(self.color)
        to_draw.append("{:.4f}".format(self.position[0]))
        to_draw.append("{:.4f}".format(self.position[1]))
        to_draw.append("{:.4f}".format(end_position[0]))
        to_draw.append("{:.4f}".format(end_position[1]))
        to_draw.append('\n')
        
        sys.stdout.write(' '.join(to_draw))



    # TODO måste vi hålla koll på om en går utanför ett visst område?
    def move(self, distance):

        new_position = self.calculate_new_position(distance)

        if self.drawing == True:

            self.draw(new_position)

        self.position = new_position



    def calculate_new_position(self, distance):

        # TODO labbeskrivning säger i "rikning v antal grader moturs från rakt högerut"
        #      men direction är från rakt norrut
        # Have to change?
        # TODO check are these actually doubles?
        x = self.position[0] + distance * math.cos(math.pi * self.direction / 180)
        y = self.position[1] + distance * math.sin(math.pi * self.direction / 180)

        return(x,y)


    ### Functions for navigating tree ###


    # TODO skrivs error in här? Eller tas det han om tidigare?

    def read_node(self, node):
        

        if node == None:
            return


        if node.value == "block":

            self.read_node(node.left)
            self.read_node(node.right)

        elif node.value == "down":

            self.drawing = True

        elif node.value == "up":

            self.drawing = False

        elif node.value == "color":

            self.color = node.left.value

        elif node.value == "forw":

            self.move(int(node.left.value))

        elif node.value == "back":

            self.move(-int(node.left.value))

        elif node.value == "left":

            self.direction = (self.direction + int(node.left.value)) % 360

        elif node.value == "right":

            self.direction = (self.direction - int(node.left.value)) % 360

        elif node.value == "reps":

            for i in range(int(node.left.value)):
                self.read_node(node.right)


