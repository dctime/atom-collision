import skin_bone

class Rigidbody(skin_bone.SkinBone):
    
    def move(self, velocity_vector:tuple):
        for index in range(len(self.nodes)):
            self.nodes[index] = (self.nodes[index][0]+velocity_vector[0], self.nodes[index][1]+velocity_vector[1])