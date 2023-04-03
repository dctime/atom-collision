class SkinBone:
    def __init__(self, nodes:list):
        self.nodes = nodes
        self.lines = []
        self._gen_lines()
    
    def get_nodes(self):
        return self.nodes
    
    def _gen_lines(self):
        for index in range(len(self.nodes)):
            if index + 1 < len(self.nodes):
                self.lines.append((self.nodes[index], self.nodes[index+1]))
            elif index + 1 == len(self.nodes):
                self.lines.append((self.nodes[index], self.nodes[0]))
            else:
                raise IndexError("Index is too large or too small")
                
    