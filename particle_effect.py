import pygame
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
    def __init__(self, particle_size:float, emit_loc:tuple, emit_speed:tuple, emit_direction:tuple, emit_angle:float):
        self.__particle_size = particle_size
        self.__emit_loc = emit_loc
        self.__emit_speed = emit_speed
        self.__emit_direction = emit_direction
        self.__emit_angle = emit_angle

