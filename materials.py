class Stone:
    def __init__(self, loc_x, loc_y, width, height, points_width, connect_max_length) -> object:
        self.loc_x = loc_x
        self.loc_y = loc_y
        self.points = self._cal_dots(loc_x, loc_y, width, height, points_width)
        self.lines = self._cal_lines(self.points, connect_max_length)
                
    def set_loc(self, x, y) -> None:
        self.loc_x = x
        self.loc_y = y
        
    def get_loc(self) -> tuple:
        return self.loc_x, self.loc_y
    
    def get_dots(self) -> list:
        return self.points
    
    def get_lines(self) -> set:
        return self.lines
    
    def _cal_dots(self, loc_x, loc_y, width, height, dots_width) -> list:
        points = []
        for i in range(height):
            for j in range(width):
                points.append((loc_x + i * dots_width, loc_y + j * dots_width))
        print(f"left up location: {loc_x}, {loc_y}")
        print("dots:", points)
        return points
    
    def _cal_lines(self, doc_locations, connect_length) -> set:
        lines = set()
        distance = lambda x_vec, y_vec: ((x_vec[0]-y_vec[0])**2+(x_vec[1]-y_vec[1])**2)**(1/2)
        for dot_first_index in range(len(self.points)):
            for dot_second_index in range(dot_first_index, len(self.points)):
                # print(f"indexs:{dot_first_index}|{dot_second_index}")
                if (distance(doc_locations[dot_first_index], doc_locations[dot_second_index]) <= connect_length):
                    lines.add((doc_locations[dot_first_index], doc_locations[dot_second_index]))
                
        # print(f"lines:{lines}")
        return lines
            
        