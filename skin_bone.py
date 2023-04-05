class SkinBone:
    def __init__(self):
        self.nodes = []
        self.lines = []
    
    def set_nodes(self, nodes:list):
        self.nodes = nodes
        self._gen_lines()
        
    def add_node(self, node:tuple):
        self.nodes.append(node)
        self._gen_lines()
        if self.is_crossover():
            print("CROSSOVER!!!!")
            self.nodes.remove(node)
            self._gen_lines()   
        
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
    
    def move(self, velocity_vector:tuple):
        for index in range(len(self.nodes)):
            self.nodes[index] = (self.nodes[index][0]+velocity_vector[0], self.nodes[index][1]+velocity_vector[1])
    
    def is_crossover(self):
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
            
    def _detect_crossover(self, line1:tuple, line2:tuple):
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
                            
    
        
        
        
        
        
        
                
    