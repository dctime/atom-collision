from block_mechanism import BlockMechanism
from leaf_blocks import CoreBlock
from block import Block
import numpy as np
np.seterr(divide='ignore', invalid='ignore')
import math

class CollisionDirector():
    def detect_and_effect_collision(self,block_mechanism_1:BlockMechanism, block_mechanism_2:BlockMechanism, time_between_frame:float):
        '''
        if there is collision, return (block1, block2)
        block1 from mecha1, block2 from mecha2
        else return None
        '''
        for _, block1 in block_mechanism_1.get_blocks().items():
            for _, block2 in block_mechanism_2.get_blocks().items():
                if not (block1._visible and block2._visible):
                    continue
                if not (self.block_collide_data(block1, block2) == None):
                    # print("Col Director:", self.block_collide_data(block1, block2))
                    effect_loc, normal_vector_block2= self.block_collide_data(block1, block2)

                    impluse = self._cal_collision_impluse(block_mechanism_1.get_momentum(), block_mechanism_2.get_momentum(), block_mechanism_1.get_angular_momentum(), block_mechanism_2.get_angular_momentum(),block_mechanism_1.get_mass(), block_mechanism_2.get_mass(), normal_vector_block2, 1).transpose()
                    # print("Col Director: impluse:", impluse)

                    force_1 = (-impluse[0]/time_between_frame, -impluse[1]/time_between_frame)
                    force_2 = (impluse[0]/time_between_frame, impluse[1]/time_between_frame)
                    block_mechanism_1.add_force(force_1, effect_loc, time_between_frame)
                    block_mechanism_2.add_force(force_2, effect_loc, time_between_frame)
                    
                    # Damage block
                    val1=math.sqrt(block_mechanism_1._momentum[0]**2 + block_mechanism_1._momentum[1]**2)
                    val2=math.sqrt(block_mechanism_2._momentum[0]**2 + block_mechanism_2._momentum[1]**2)
                    val = (val1+val2)/5000
                    block1.damage_block(val)
                    block2.damage_block(val)
                    #print("damage: ",val)

                    # Remove destroyed blocks
                    if block1.get_status()==0:
                        block_mechanism_1.remove_block(block1)

                    if block2.get_status()==0:
                        block_mechanism_2.remove_block(block2)

                    return (block1, block2)
        return None
                
    def block_collide_data(self, block1:Block, block2:Block) -> tuple:
        '''
        return node:tuple, normal_vector, the direction of force of block2:np.ndarray
        if doesnt collide, returns None
        '''
        # block2's node in block1
        IMPACT_LINE_STRETCH = 100
        for node_index in range(len(block2.get_nodes())):
            if self.is_node_in_block(block2.get_nodes()[node_index], block1):
                node = tuple(block2.get_nodes()[node_index])
                impact_line = [block2.get_previous_nodes()[node_index], tuple(block2.get_nodes()[node_index])]
                impact_line[0] = ((impact_line[0][0]-impact_line[1][0])*IMPACT_LINE_STRETCH+impact_line[1][0], (impact_line[0][1]-impact_line[1][1])*IMPACT_LINE_STRETCH+impact_line[1][1])
                impact_line[1] = ((impact_line[1][0]-impact_line[0][0])*IMPACT_LINE_STRETCH+impact_line[0][0], (impact_line[1][1]-impact_line[0][1])*IMPACT_LINE_STRETCH+impact_line[0][1])
                for line in block1.get_lines():
                    if self._detect_crossover(line, impact_line):
                        # #print(node, self._normal_vector_for_impactor(impact_line, line))
                        return node, self._normal_vector_for_impactor(impact_line, line)
                return None
        return None

    def is_node_in_block(self, node:tuple, block:Block) -> bool:
        '''
        if there is a node which is in the block, return the node
        '''
        nodes = block.get_nodes()
        if not ((nodes[0][0]-nodes[1][0]) == 0 or (nodes[2][0]-nodes[1][0]) == 0):
            ma = (nodes[0][1]-nodes[1][1])/(nodes[0][0]-nodes[1][0])
            b1 = nodes[1][1]-ma*nodes[1][0]
            b2 = nodes[2][1]-ma*nodes[2][0]
            bt = node[1]-ma*node[0]
            if not ((b2 >= bt and bt >= b1) or (b1 >= bt and bt >= b2)):
                return False
            
            mb = ((nodes[2][1]-nodes[1][1])/(nodes[2][0]-nodes[1][0]))
            b1 = nodes[1][1]-mb*nodes[1][0]
            b0 = nodes[0][1]-mb*nodes[0][0]
            btt = node[1]-mb*node[0]
            if not ((b1 >= btt and btt >= b0) or (b0 >= btt and btt >= b1)):
                return False
        
            return True
        else:
            # x coor
            if not ((nodes[1][0] >= node[0] and node[0] >= nodes[3][0]) or (nodes[3][0] >= node[0] and node[0] >= nodes[1][0])):
                return False
            
            # y coor
            if not ((nodes[1][1] >= node[1] and node[1] >= nodes[3][1]) or (nodes[3][1] >= node[1] and node[1] >= nodes[1][1])):
                return False
            
            return True
        
    def _normal_vector_for_impactor(self, impact_line, hit_line) -> np.ndarray:
        '''
        hit line been hit by node
        '''
        v1 = np.array([impact_line[1][0]-impact_line[0][0], impact_line[1][1]-impact_line[1][0]]).transpose()
        v2 = np.array([hit_line[1][0]-hit_line[0][0], hit_line[1][1]-hit_line[1][0]]).transpose()
        vn = v1 - (np.dot(v1, v2)/np.dot(v2, v2))*v2
        vn_length = np.linalg.norm(vn)

        if vn_length == 0:
            return 0
        else:
            vn = -1*(vn/vn_length)
            return vn
        
    def _array_to_tuple(self, arr):
        if isinstance(arr, np.ndarray):
            return tuple(self._array_to_tuple(e) for e in arr)
        else:
            return arr
              
    def _detect_crossover(self, line1:tuple, line2:tuple) -> bool:
        '''
        line is made of two points ((x1, y1), (x2, y2))
        '''
        # ax + by = c
        # y - y0 = m(x - x0)
        # (y-y0) = mx - mx0
        # y-y0-mx = -mx0
        # y - mx = y0 - mx0
        # #print(f"line1:{line1}")
        # #print(f"line2:{line2}")
        line2_points_for_line1 = False
        try:
            m1 = (line1[1][1]-line1[0][1])/(line1[1][0]-line1[0][0])
            line1_equation = lambda x, y: y - (line1[1][1]-line1[0][1])/(line1[1][0]-line1[0][0])*x
            answer_if_on_line1 = line1[0][1]-m1*line1[0][0]
            
            if not ((line1_equation(line2[0][0], line2[0][1]) > answer_if_on_line1 and line1_equation(line2[1][0], line2[1][1]) > answer_if_on_line1) or\
                (line1_equation(line2[0][0], line2[0][1]) < answer_if_on_line1 and line1_equation(line2[1][0], line2[1][1]) < answer_if_on_line1)):
                # #print("CROSSOVER")
                line2_points_for_line1 = True
        except: # ZeroDivisionError:
            x = line1[0][0]
            if not ((line2[0][0] > x and line2[1][0] > x) or (line2[0][0] < x and line2[1][0] < x)):
                # #print("CROSSOVER")
                line2_points_for_line1 = True
                
        line1_points_for_line2 = False
        try:
            m2 = (line2[1][1]-line2[0][1])/(line2[1][0]-line2[0][0])
            line2_equation = lambda x, y: y - (line2[1][1]-line2[0][1])/(line2[1][0]-line2[0][0])*x
            answer_if_on_line2 = line2[0][1]-m2*line2[0][0]
            
            if not ((line2_equation(line1[0][0], line1[0][1]) > answer_if_on_line2 and line2_equation(line1[1][0], line1[1][1]) > answer_if_on_line2) or\
                (line2_equation(line1[0][0], line1[0][1]) < answer_if_on_line2 and line2_equation(line1[1][0], line1[1][1]) < answer_if_on_line2)):
                # #print("CROSSOVER")
                line1_points_for_line2 = True
        except: # ZeroDivisionError:
            x = line2[0][0]
            if not ((line1[0][0] > x and line1[1][0] > x) or (line1[0][0] < x and line1[1][0] < x)):
                # #print("CROSSOVER")
                line1_points_for_line2 = True
                
        return line2_points_for_line1 and line1_points_for_line2
    
    def _cal_collision_impluse(self, momentum1:tuple, momentum2:tuple, angular_momentum1:float, angular_momentum2:float, mass1:float, mass2:float, normal_vector:np.ndarray, e:float) -> np.ndarray:
        '''
        e must be 0 to 1
        normal_vector is the back direction of the opponent's direction
        '''
        SCALAR_MIN = 1000
        momentum1 = np.array(momentum1).transpose()
        momentum2 = np.array(momentum2).transpose()
        
        scalar = ((1+e)*np.dot(((momentum1*(1/mass1))-(momentum2*(1/mass2))), normal_vector))/((1/mass1)+(1/mass2))
        scalar += abs((1+e)*(((angular_momentum1*(1/mass1))-(angular_momentum2*(1/mass2)))))/((1/mass1)+(1/mass2))
        #print("Col dir: Scalar:", scalar)
        if np.linalg.norm(scalar) < SCALAR_MIN:
            if np.linalg.norm(scalar) == 0:
                scalar = scalar*SCALAR_MIN
            else:
                scalar = scalar*(SCALAR_MIN/np.linalg.norm(scalar))

        impluse = scalar*normal_vector
        return impluse
    