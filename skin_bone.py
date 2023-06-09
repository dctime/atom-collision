import pygame
import copy

class SkinBone:
    def __init__(self, nodes_max_length=10):
        '''
        nodes_max_length: the distance between the two points when calls the fill_nodes method
        the higher the value the smoother the crack is
        high value -> clay, low value -> wood

        self.nodes
        example: [(1, 2), (1, 3), (2, 3)]
        self.lines
        example: [((1, 2), (1, 3)), ((1, 3), (2, 3)), ((2, 3), (1, 2))]
        '''
        self._previous_nodes = []
        self.nodes = []
        self.lines = []
        self.nodes_max_length = nodes_max_length

    def render(self, screen, color, debug_color=(255, 0, 0)):
        if len(self.get_nodes()) == 1:
            pygame.draw.circle(screen, debug_color, self.get_nodes()[0], 3)
        elif len(self.get_nodes()) == 2:
            pygame.draw.line(screen, color, self.get_nodes()[0], self.get_nodes()[1])
            pygame.draw.circle(screen, debug_color, self.get_nodes()[0], 3)
            pygame.draw.circle(screen, debug_color, self.get_nodes()[1], 3)
        elif len(self.get_nodes()) > 2:
            pygame.draw.polygon(screen, color, self.get_nodes(), 0)
    
    def set_nodes(self, nodes:list, fill_nodes=False):
        '''
        example: [(1, 2), (1, 3), (2, 3)]
        '''
        self._previous_nodes = copy.deepcopy(self.nodes)
        self.nodes = nodes
        self._gen_lines()
        if fill_nodes:
            self.fill_nodes()
        
    def add_node(self, node:tuple):
        self.nodes.append(node)
        self._gen_lines()
        if self.is_crossover():
            print("CROSSOVER!!!!")
            self.nodes.remove(node)
            self._gen_lines()

    def get_previous_nodes(self):
        return self._previous_nodes
        
    def get_nodes(self):
        return self.nodes
    
    def _gen_lines(self):
        self.lines = []
        if len(self.nodes) > 1:
            for index in range(len(self.nodes)):
                if index + 1 < len(self.nodes):
                    self.lines.append((self.nodes[index], self.nodes[index+1]))
                    # print(f"ADD lines, now lines:{self.lines}")
                elif index + 1 == len(self.nodes) and len(self.nodes) > 2:
                    self.lines.append((self.nodes[index], self.nodes[0]))
                    # print(f"ADD lines, now lines:{self.lines}")
        # print(f"LINES:{self.lines}")
    
    def is_crossover(self) -> bool:
        is_crossover = False
        
        if len(self.lines) > 3:
            # print(f"Lines:{self.lines}")
            new_line1 = self.lines[-1]
            new_line2 = self.lines[-2]
            for line in self.lines[1:-2]:
                if self._detect_crossover(line, new_line1):
                    is_crossover = True
                    break
                
            for line in self.lines[:-3]:
                if self._detect_crossover(line, new_line2):
                    is_crossover = True
                    break
                
        return is_crossover
    
    def fill_nodes(self) -> None:
        changed = False
        nodes = self.nodes
        for index in range(len(nodes)-1, -1, -1):
            node1 = ()
            node2 = ()
            if index + 1 >= len(nodes):
                node1 = (nodes[index])
                node2 = (nodes[0])
            else:
                node1 = (nodes[index])
                node2 = (nodes[index+1])
                
            distance = lambda vector1, vector2: ((vector2[0] - vector1[0])**2 + (vector2[1] - vector1[1])**2)**(1/2)
            middle = lambda vector1, vector2: ((vector1[0] + vector2[0])/2, (vector1[1]+vector2[1])/2)
            if distance(node1, node2) > self.nodes_max_length:
                self.nodes.insert(index+1, middle(node1, node2))
                # print(f"NODES:{self.nodes}")
                changed = True
                break
            
        if changed:
            self.fill_nodes()
                  
    def _detect_crossover(self, line1:tuple, line2:tuple) -> bool:
        '''
        line is made of two points ((x1, y1), (x2, y2))
        '''
        # ax + by = c
        # y - y0 = m(x - x0)
        # (y-y0) = mx - mx0
        # y-y0-mx = -mx0
        # y - mx = y0 - mx0
        # print(f"line1:{line1}")
        # print(f"line2:{line2}")
        line2_points_for_line1 = False
        try:
            m1 = (line1[1][1]-line1[0][1])/(line1[1][0]-line1[0][0])
            line1_equation = lambda x, y: y - (line1[1][1]-line1[0][1])/(line1[1][0]-line1[0][0])*x
            answer_if_on_line1 = line1[0][1]-m1*line1[0][0]
            
            if not ((line1_equation(line2[0][0], line2[0][1]) > answer_if_on_line1 and line1_equation(line2[1][0], line2[1][1]) > answer_if_on_line1) or\
                (line1_equation(line2[0][0], line2[0][1]) < answer_if_on_line1 and line1_equation(line2[1][0], line2[1][1]) < answer_if_on_line1)):
                # print("CROSSOVER")
                line2_points_for_line1 = True
        except ZeroDivisionError:
            x = line1[0][0]
            if not ((line2[0][0] > x and line2[1][0] > x) or (line2[0][0] < x and line2[1][0] < x)):
                # print("CROSSOVER")
                line2_points_for_line1 = True
                
        line1_points_for_line2 = False
        try:
            m2 = (line2[1][1]-line2[0][1])/(line2[1][0]-line2[0][0])
            line2_equation = lambda x, y: y - (line2[1][1]-line2[0][1])/(line2[1][0]-line2[0][0])*x
            answer_if_on_line2 = line2[0][1]-m2*line2[0][0]
            
            if not ((line2_equation(line1[0][0], line1[0][1]) > answer_if_on_line2 and line2_equation(line1[1][0], line1[1][1]) > answer_if_on_line2) or\
                (line2_equation(line1[0][0], line1[0][1]) < answer_if_on_line2 and line2_equation(line1[1][0], line1[1][1]) < answer_if_on_line2)):
                # print("CROSSOVER")
                line1_points_for_line2 = True
        except ZeroDivisionError:
            x = line2[0][0]
            if not ((line1[0][0] > x and line1[1][0] > x) or (line1[0][0] < x and line1[1][0] < x)):
                # print("CROSSOVER")
                line1_points_for_line2 = True
                
        return line2_points_for_line1 and line1_points_for_line2
                            
    
        
        
        
        
        
        
                
    