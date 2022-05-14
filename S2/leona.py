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
        

        # TODO kanske kolla att allt blir bra utan negativa nollor?
        to_draw = []
        to_draw.append(self.color)
        to_draw.append("{:.4f}".format(self.position[0]))
        to_draw.append("{:.4f}".format(self.position[1]))
        if end_position[0] > -0.00001 and end_position[0] < 0:
            to_draw.append("{:.4f}".format(-end_position[0]))
        else:
            to_draw.append("{:.4f}".format(end_position[0]))
        to_draw.append("{:.4f}".format(end_position[1]))

        
        sys.stdout.write(' '.join(to_draw))
        sys.stdout.write('\n')



    def move(self, distance):

        new_position = self.calculate_new_position(distance)

        if self.drawing == True:

            self.draw(new_position)

        self.position = new_position



    def calculate_new_position(self, distance):

        x = self.position[0] + distance * math.cos(math.pi * self.direction / 180)
        y = self.position[1] + distance * math.sin(math.pi * self.direction / 180)

        return(x,y)


    ### Functions for navigating tree ###


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


