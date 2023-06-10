from controllable_mechanism import ControllableMechansim
from controllable_mechanism_builder import ControllableMechansimBuilder
from collision_director import CollisionDirector
from gravity_director import GravityDirector
from color import Color
from sound import Sounds
from particle_effect import GravityParticleEffect
import pygame
import random



class Actions():
    CORE_MOVE_UP = "core_move_up"
    CORE_MOVE_DOWN = "core_move_down"
    CORE_MOVE_LEFT = "core_move_left"
    CORE_MOVE_RIGHT = "core_move_right"

class KeyGroups():
    ThrusterKeys = (pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT)

class Game:
    def __init__(self, pygame_screen:pygame.Surface, time_between_frame:float, zero_vector:tuple, unit_size:int, background: str = None) -> None:
        self._players = []  # list of players(BlockMechanism)
        self._builders = [ControllableMechansimBuilder(), ControllableMechansimBuilder()] # list of ControllableMechansimBuilder
        self._builder_index = 0
        self._objects = []   # list of objects(like bullet)
        self._phase = "build"
        self._background = background
        self._screen = pygame_screen
        self._collision_director = CollisionDirector()
        self._gravity_director = GravityDirector(10**(10), (0, 0), time_between_frame)
        self._time_between_frame = time_between_frame
        self._zero_vector = zero_vector
        self._unit_size = unit_size
        self._running = True
        self._gravity_particle_effect = GravityParticleEffect(pygame_screen, max(pygame_screen.get_size()[0], pygame_screen.get_size()[1]), (0, 0), 3)
        
    def alive(self)->tuple:
        alive1 = self.get_player(0)._core._visible
        alive2 = self.get_player(1)._core._visible
        return (alive1,alive2)
    
    def run_build(self)->None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            elif event.type == pygame.KEYDOWN:
                key = event.key
                self.__build_key_events(key)

    def run_battle(self,collision_delay,COLLISION_DELAY_MAX)->None:
        # force stuff
        for player in self._players:
            self._gravity_director.add_gravity(player)

        # collision stuff
        if collision_delay == 0:
            collision_delay = COLLISION_DELAY_MAX
            for index1 in range(len(self._players)-1):
                for index2 in range(index1+1, len(self._players)):
                    collision_report = self._collision_director.detect_and_effect_collision(self._players[index1], self._players[index2], self._time_between_frame)
                    if not (collision_report == None):
                        self.__collision_events(collision_report)
        
        
        self.__battle_key_events()

        # moving stuff
        for player in self._players:
            player.move_by_physics(self._time_between_frame)

        # particle stuff
        self._gravity_particle_effect.render(self._zero_vector, self._unit_size)
        
        # Check if the game is end
        alive=self.alive()
        if not (alive[0] and alive[1]):
            self.set_phase("end")

    def run_end(self)->None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    self._running = False
        pass

    def run(self) -> None:
        # Call this in main loop
        collision_delay = 10
        COLLISION_DELAY_MAX = 10

        clock = pygame.time.Clock()
        
        
        game_time = 0

        while self._running:
            # shut down the game
            # for event in pygame.event.get():
            #     if event.type == pygame.QUIT:
            #         running = False

            # #print("Main: GAME TIME:", game_time)
            # set up the background
            self._screen.fill((0, 0, 0))
            
            if self.get_phase()=="build":
                self.run_build()
            elif self.get_phase()=="battle":
                self.run_battle(collision_delay,COLLISION_DELAY_MAX)
                if collision_delay:
                    collision_delay -= 1

            elif self.get_phase()=="end":
                self.run_end()
            
            # render stuff
            self.__draw(self._zero_vector, self._unit_size)

            # ======== DEBUGGING ==========
            # Draw debugging points on the screen
            # pygame.draw.circle(self._screen, Color.MID_SCREEN_COLOR, self._zero_vector, 3)

            # Draw center of mass of player1
            #pygame.draw.circle(self._screen, Color.CENTER_OF_MASS_COLOR, change_normalized_into_real(self._zero_vector, self._unit_size, self._players[0].get_center_of_mass_coor()), 3)
            # Draw center of mass of player2
            #pygame.draw.circle(self._screen, Color.CENTER_OF_MASS_COLOR, change_normalized_into_real(self._zero_vector, self._unit_size, self._players[1].get_center_of_mass_coor()), 3)
            # draw every blocks coor
            #for _, block in self._players[0].get_blocks().items():
            #    pygame.draw.circle(self._screen, Color.BLOCK_COOR_COLOR, change_normalized_into_real(self._zero_vector, self._unit_size, block.get_coor()), 2)

            
            # Update screen
            pygame.display.flip()
            clock.tick(1/self._time_between_frame) # it doesnt not become super fast idk why
            game_time += 1

        # Quit Pygame
        pygame.quit()
    
    def add_players(self, player1:ControllableMechansim, player2:ControllableMechansim):
        self._players = []
        player1.set_oppo(player2)
        player2.set_oppo(player1)
        self._players.append(player1)
        self._players.append(player2)

    def get_player(self, index: int):
        # Return players[index](BlockAssembly)
        return self._players[index]

    def add_object(self, object) -> None:
        # Add object to objects
        self._objects.append(object)

    def remove_object(self, object) -> None:
        # Remove object from objects
        self._objects.remove(object)

    def get_phase(self) -> str:
        return self._phase

    def set_phase(self, phase: str) -> None:
        self._phase = phase

    def is_valid(self, instruction) -> bool:
        # Check if the instruction is valid for current stage
        condition = None
        if condition:
            return False
        return True

    def act(self, player:ControllableMechansim, action:str) -> None:
        # Apply action on the player
        if action == Actions.CORE_MOVE_UP:
            player.core_move_up(self._time_between_frame)

        elif action == Actions.CORE_MOVE_DOWN:
            player.core_move_down(self._time_between_frame)

        elif action == Actions.CORE_MOVE_LEFT:
            player.core_move_left(self._time_between_frame)
        
        elif action == Actions.CORE_MOVE_RIGHT:
            player.core_move_right(self._time_between_frame)

    def __draw(self, zero_vector:tuple, unit_size:int) -> None:
        # Draw background, players and objects(follow the order)
        # render called below are all undefined yet

        # TODO: make background alive
        # self._background.render()

        for object in self._objects:
            # TODO: add zero vector and unit size so the game wont break
            object.render(self._screen, zero_vector, unit_size)

        for player in self._players:
            player.render(self._screen, zero_vector, unit_size)

        if self.get_phase() == "build":
            change_normalized_into_real = lambda zero_vector, unit_size, target_vector:(target_vector[0]*unit_size+zero_vector[0], target_vector[1]*unit_size+zero_vector[1])
            builder = self._builders[self._builder_index]
            builder.render(self._screen,zero_vector,unit_size, change_normalized_into_real(zero_vector,unit_size,builder._cursor))
            
    def __build_key_events(self,key):
        # Move cursor
        if key == pygame.K_w:
            self._builders[self._builder_index].move_cursor("up")
        if key == pygame.K_s:
            self._builders[self._builder_index].move_cursor("down")
        if key == pygame.K_a:
            self._builders[self._builder_index].move_cursor("left")
        if key == pygame.K_d:
            self._builders[self._builder_index].move_cursor("right")

        # Set texture
        if key == pygame.K_1:
            self._builders[self._builder_index].set_block_type("wood")
        if key == pygame.K_2:
            self._builders[self._builder_index].set_block_type("stone")

        # Add block
        if key == pygame.K_UP:
            self._builders[self._builder_index].add_block_dir("up")
        if key == pygame.K_DOWN:
            self._builders[self._builder_index].add_block_dir("down")
        if key == pygame.K_LEFT:
            self._builders[self._builder_index].add_block_dir("left")
        if key == pygame.K_RIGHT:
            self._builders[self._builder_index].add_block_dir("right")
        
        # Delete block
        if key == pygame.K_DELETE:
             self._builders[self._builder_index].delete_block()
        
        # Swith to battle phase
        if key == pygame.K_RETURN:
            if self._builder_index == 0:
                 self._builder_index = 1
            else:
                player1=self._builders[0].build()
                player2=self._builders[1].build()
                self.add_players(player1,player2)
                player1.move_to((-5,0))
                player2.move_to((5,0))
                self.set_phase("battle")
        


    def __battle_key_events(self):
        # key events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    self._running = False

            if event.type == pygame.KEYDOWN:
                for key in KeyGroups.ThrusterKeys:
                    if event.key == key:
                        Sounds.THRUSTER_BURN.play()
                        print("WHOOOSE GAME")

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
                self.act(self._players[0], Actions.CORE_MOVE_UP)

        if keys[pygame.K_s]:
                self.act(self._players[0], Actions.CORE_MOVE_DOWN)
                
        if keys[pygame.K_a]:
                self.act(self._players[0], Actions.CORE_MOVE_LEFT)

        if keys[pygame.K_d]:
                self.act(self._players[0], Actions.CORE_MOVE_RIGHT)

        if keys[pygame.K_UP]:
                self.act(self._players[1], Actions.CORE_MOVE_UP)

        if keys[pygame.K_DOWN]:
                self.act(self._players[1], Actions.CORE_MOVE_DOWN)

        if keys[pygame.K_LEFT]:
                self.act(self._players[1], Actions.CORE_MOVE_LEFT)

        if keys[pygame.K_RIGHT]:
                self.act(self._players[1], Actions.CORE_MOVE_RIGHT)

    def __collision_events(self, collision_report):
        '''
        called when collision happnens
        '''
        if random.randint(0, 1):
            Sounds.BUMP1.play()
        else:
            Sounds.BUMP2.play()
