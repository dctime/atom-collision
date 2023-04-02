class Bone:
    def __init__(self, loc_x, loc_y, width, height, points_width, connect_max_length) -> object:
        self.loc_x = loc_x
        self.loc_y = loc_y
        
        self.lines = set()
        self.points = []
        
        self.connect_max_length = connect_max_length
        
        self._init_dots(self.loc_x, self.loc_y, width, height, points_width)
        self._update_lines(self.points, connect_max_length)

    def set_loc(self, x, y) -> None:
        self.loc_x = x
        self.loc_y = y

    def get_loc(self) -> tuple:
        return self.loc_x, self.loc_y

    def get_dots(self) -> list:
        return self.points

    def get_lines(self) -> set:
        return self.lines
    
    def print_dots(self) -> None:
        index = 0
        for dot in self.points:
            print(f"{index}|{dot}")
            index += 1
        
    def remove_dot(self, point_loc_x_or_id, point_loc_y=None) -> None:
        if point_loc_y == None:
            self.points.pop(point_loc_x_or_id)
        else:
            self.points.remove((point_loc_x_or_id, point_loc_y))
            
        self._update_lines(self.points, self.connect_max_length)

    def _init_dots(self, loc_x, loc_y, width, height, dots_width) -> list:
        
        points = []
        for i in range(height):
            for j in range(width):
                points.append((loc_x + i * dots_width, loc_y + j * dots_width))
        # print(f"left up location: {loc_x}, {loc_y}")
        # print("dots:", points)
        self.points = points

    def _update_lines(self, doc_locations, connect_length) -> set:
        
        lines = set()

        def distance(x_vec, y_vec): return (
            (x_vec[0]-y_vec[0])**2+(x_vec[1]-y_vec[1])**2)**(1/2)
        for dot_first_index in range(len(self.points)):
            for dot_second_index in range(dot_first_index, len(self.points)):
                # print(f"indexs:{dot_first_index}|{dot_second_index}")
                if (distance(doc_locations[dot_first_index], doc_locations[dot_second_index]) <= connect_length):
                    lines.add(
                        (doc_locations[dot_first_index], doc_locations[dot_second_index]))

        # print(f"lines:{lines}")
        self.lines = lines
