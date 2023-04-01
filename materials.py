class Stone:
    """A class representing a stone object.

    This class has methods for setting and getting the location of the stone,
    as well as calculating its points and lines.

    Attributes:
        loc_x (int): The x-coordinate of the stone's location.
        loc_y (int): The y-coordinate of the stone's location.
        points (list): A list of points representing the stone.
        lines (set): A set of lines connecting the points of the stone.
    """

    def __init__(self, loc_x, loc_y, width, height, points_width, connect_max_length) -> object:
        """Initializes a new Stone object.

        Args:
            loc_x (int): The x-coordinate of the stone's location.
            loc_y (int): The y-coordinate of the stone's location.
            width (int): The width of the stone.
            height (int): The height of the stone.
            points_width (int): The distance between points on the stone.
            connect_max_length (int): The maximum length of a line connecting two points on the stone.
        """
        self.loc_x = loc_x
        self.loc_y = loc_y
        self.points = self._cal_dots(loc_x, loc_y, width, height, points_width)
        self.lines = self._cal_lines(self.points, connect_max_length)

    def set_loc(self, x, y) -> None:
        """Sets the location of the stone.

        Args:
            x (int): The new x-coordinate of the stone's location.
            y (int): The new y-coordinate of the stone's location.
        """
        self.loc_x = x
        self.loc_y = y

    def get_loc(self) -> tuple:
        """Returns the location of the stone.

        Returns:
            tuple: A tuple containing the x and y coordinates of the stone's location.
        """
        return self.loc_x, self.loc_y

    def get_dots(self) -> list:
        """Returns the points representing the stone.

        Returns:
            list: A list of points representing the stone.
        """
        return self.points

    def get_lines(self) -> set:
        """Returns the lines connecting the points of the stone.

        Returns:
            set: A set of lines connecting the points of the stone.
        """
        return self.lines

    def _cal_dots(self, loc_x, loc_y, width, height, dots_width) -> list:
        """Calculates and returns the points representing the stone.

        Args:
            loc_x (int): The x-coordinate of the stone's location.
            loc_y (int): The y-coordinate of the stone's location.
            width (int): The width of the stone.
            height (int): The height of the stone.
            dots_width (int): The distance between points on the stone.

        Returns:
            list: A list of points representing the stone.
        """
        points = []
        for i in range(height):
            for j in range(width):
                points.append((loc_x + i * dots_width, loc_y + j * dots_width))
        print(f"left up location: {loc_x}, {loc_y}")
        print("dots:", points)
        return points

    def _cal_lines(self, doc_locations, connect_length) -> set:
        """Calculates and returns the lines connecting the points of the stone.

        Args:
            doc_locations (list): A list of points representing the stone.
            connect_length (int): The maximum length of a line connecting two points on the stone.

        Returns:
            set: A set of lines connecting the points of the stone.
        """
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
        return lines
