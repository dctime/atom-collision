import pygame
import random
from color import Color

change_normalized_into_real = lambda zero_vector, unit_size, target_vector:(target_vector[0]*unit_size+zero_vector[0], target_vector[1]*unit_size+zero_vector[1])

class GravityParticleEffect():
    def __init__(self, max_radius:float, loc:tuple, width:float):
        self.__max_radius = max_radius
        self.__radius = max_radius
        self.__loc = loc
        self.__width = width

    def render(self, screen, zero_vector:tuple, unit_size:float):
        pygame.draw.circle(screen, Color.GRAVITY_PARTICLE_COLOR, change_normalized_into_real(zero_vector, unit_size, self.__loc), 5, 0)
        pygame.draw.circle(screen, Color.GRAVITY_PARTICLE_COLOR, change_normalized_into_real(zero_vector, unit_size, self.__loc), self.__radius, self.__width)
        self.__radius -= 0.5
        if self.__radius <= 0:
            self.__radius = self.__max_radius

class ThrusterParticleEffect():
    def __init__(self, particle_size:float, emit_loc:tuple, emit_velocity:tuple, lifetime:int):
        self.__particle_size = particle_size
        self.__emit_loc = emit_loc
        self.__emit_velocity = emit_velocity
        self.__lifetime = lifetime
        self.__particle_loc = emit_loc

    def render(self, screen, zero_vector:tuple, unit_size:float) -> bool:
        '''
        True if can render, False if cant
        '''
        if self.__lifetime > 0:
            pygame.draw.circle(screen, Color.THRUSTER_PARTICLE_COLOR, change_normalized_into_real(zero_vector, unit_size, self.__particle_loc), self.__particle_size*unit_size)
            self.__particle_loc = (self.__particle_loc[0]+self.__emit_velocity[0], self.__particle_loc[1]+self.__emit_velocity[1])
            self.__lifetime -= 1
            return True
        else:
            return False
        
class ThrusterParticlesEffect():
    def __init__(self):
        self.__particles = []
        self.__current_emit_delay = 0

    def emit(self, emit_loc:tuple, emit_velocity:tuple, error_tolerance:float, particle_size:float, emit_delay:float, lifetime:int):
        self.__current_emit_delay -= 1
        if self.__current_emit_delay < 0:
            self.__current_emit_delay = emit_delay

            randomness_velocity = (emit_velocity[0]+random.uniform(-error_tolerance, error_tolerance), emit_velocity[1]+random.uniform(-error_tolerance, error_tolerance))
            self.__particles.append(ThrusterParticleEffect(particle_size, emit_loc, randomness_velocity, lifetime))
        
        

    def render(self, screen, zero_vector, unit_size):
        for particle in self.__particles:
            if not particle.render(screen, zero_vector, unit_size):
                del particle

        

