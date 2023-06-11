from controllable_mechanism import ControllableMechansim
from controllable_mechanism_builder import ControllableMechansimBuilder
from collision_director import CollisionDirector
from gravity_director import GravityDirector
from color import Color
from sound import Sounds
from particle_effect import GravityParticleEffect, ThrusterParticlesEffect
import pygame
import random

WIDTH = 1200
HEIGHT = 800
CENTER = (WIDTH//2, HEIGHT//2)

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
        self._gravity_particle_effect = GravityParticleEffect(max(pygame_screen.get_size()[0], pygame_screen.get_size()[1]), (0, 0), 3)
        self._origin_hp = []
        self._thruster_particle_effect = ThrusterParticlesEffect()
        self._player_thruster_particle_effect = {}
        self._battle_time = 0
        self._battle_bgm_channel = pygame.mixer.find_channel()

        
    def alive(self)->tuple:
        alive1 = self.get_player(0)._core._visible
        alive2 = self.get_player(1)._core._visible
        return (alive1,alive2)
    
    def run_build(self)->None:
        # Draw coin GUI
        font = pygame.font.Font(None,32)
        coin_text = font.render("Coin     "+str(self._builders[self._builder_index]._coin),True,(255,255,255))
        hint_move_cursor_text = font.render("WASD: Move cursor",True,(255,255,255))
        hint_cursor_dot_text = font.render("Red: Wood, Green: Stone",True,(255,255,255))
        hint_add_block_text = font.render("Direction: Add block",True,(255,255,255))

        coin_text_rect = coin_text.get_rect()
        coin_text_rect.topleft = (0,0)
        hint_move_cursor_text_rect = hint_move_cursor_text.get_rect()
        hint_move_cursor_text_rect.topleft = (0, 40)
        hint_cursor_dot_text_rect = hint_cursor_dot_text.get_rect()
        hint_cursor_dot_text_rect.topleft = (0,80)
        hint_add_block_text_rect = hint_add_block_text.get_rect()
        hint_add_block_text_rect.topleft = (0,120)

        self._screen.blit(coin_text, coin_text_rect)
        self._screen.blit(hint_move_cursor_text, hint_move_cursor_text_rect)
        self._screen.blit(hint_cursor_dot_text, hint_cursor_dot_text_rect)
        self._screen.blit(hint_add_block_text, hint_add_block_text_rect)


        # render stuff
        self.__draw_blocks(self._zero_vector, self._unit_size)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            elif event.type == pygame.KEYDOWN:
                key = event.key
                self.__build_key_events(key)

    def run_battle(self,collision_delay,COLLISION_DELAY_MAX)->None:
        self._battle_time += 1

        if self._battle_time == 3000:
            self._battle_bgm_channel.play(Sounds.BATTLE_BGM)

        # render stuff
        self._gravity_particle_effect.render(self._screen, self._zero_vector, self._unit_size)
        self.__draw_blocks(self._zero_vector, self._unit_size)
        for player in self._players:
            self._player_thruster_particle_effect[player].render(self._screen, self._zero_vector, self._unit_size)

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
        
        # Check if the game is end
        alive=self.alive()
        if not (alive[0] and alive[1]):
            self.set_phase("end")

    def run_end(self)->None:
        # fade the bgm out
        self._battle_bgm_channel.fadeout(10000)

        # render stuff
        self.__draw_blocks(self._zero_vector, self._unit_size)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    self._running = False
        
        # Calculate score
        hp1 = self.get_player(0).total_hp()
        hp2 = self.get_player(1).total_hp()
        score1 = int(hp1 + (self._origin_hp[1]-hp2))
        score2 = int(hp2 + (self._origin_hp[0]-hp1))

        # Display results
        result_surface = pygame.Surface((600,400))
        result_surface.fill((16,16,16))
        result_surface.set_alpha(128)
        result_surface_rect = result_surface.get_rect()
        result_surface_rect.center = CENTER
        self._screen.blit(result_surface, result_surface_rect)

        # Winner
        font = pygame.font.Font(None,32)
        win1_text = font.render("Play 1 is the winner",True,(255,255,255))
        win2_text = font.render("Play 2 is the winner",True,(255,255,255))
        draw_text = font.render("Nobody is the winner",True,(255,255,255))
        win_text_rect = win1_text.get_rect()
        win_text_rect.center = tuple(map(lambda x,y:x-y, CENTER,(0,80)))
        alive = self.alive()
        if alive[0]:
             self._screen.blit(win1_text, win_text_rect)
        elif alive[1]:
             self._screen.blit(win2_text, win_text_rect)
        else:
             self._screen.blit(draw_text, win_text_rect)

        # Score
        score_text = font.render("SCORE",True,(255,255,255))
        score_text_rect = score_text.get_rect()
        score_text_rect.center = tuple(map(lambda x,y:x-y, CENTER,(0,40)))
        self._screen.blit(score_text, score_text_rect)

        result1_text = font.render("Player 1     "+ str(score1),True,(255,255,255))
        result1_text_rect = result1_text.get_rect()
        result1_text_rect.center = tuple(map(lambda x,y:x-y, CENTER,(0,0)))
        result2_text = font.render("Player 2     "+ str(score2),True,(255,255,255))
        result2_text_rect = result2_text.get_rect()
        result2_text_rect.center = tuple(map(lambda x,y:x-y, CENTER,(0,-40)))
        self._screen.blit(result1_text, result1_text_rect)
        self._screen.blit(result2_text, result2_text_rect)

    def run(self) -> None:
        # Call this in main loop
        collision_delay = 10
        COLLISION_DELAY_MAX = 10

        clock = pygame.time.Clock()

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
            if self.get_phase()=="end":
                 self.run_end()

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

        # Quit Pygame
        pygame.quit()
    
    def add_players(self, player1:ControllableMechansim, player2:ControllableMechansim):
        self._players = []
        player1.set_oppo(player2)
        player2.set_oppo(player1)
        self._players.append(player1)
        self._players.append(player2)
        for player in self._players:
            self._player_thruster_particle_effect[player] = ThrusterParticlesEffect()


    def build_players(self):
        player1=self._builders[0].build()
        player2=self._builders[1].build()
        self.add_players(player1,player2)
        player1.move_to((-5,0))
        player2.move_to((5,0))
        player1.add_force((100, 100), (0, 300), 1)
        player2.add_force((-100, -100), (0, -300), 1)
        self._origin_hp.extend([player1.total_hp(),player2.total_hp()])
        self.set_phase("battle")

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
            self._player_thruster_particle_effect[player].emit(player.get_coor(), (0, 0.03), 0.02, 0.1, 5, 100)

        elif action == Actions.CORE_MOVE_DOWN:
            player.core_move_down(self._time_between_frame)
            self._player_thruster_particle_effect[player].emit(player.get_coor(), (0, -0.03), 0.02, 0.1, 5, 100)

        elif action == Actions.CORE_MOVE_LEFT:
            player.core_move_left(self._time_between_frame)
            self._player_thruster_particle_effect[player].emit(player.get_coor(), (0.03, 0), 0.02, 0.1, 5, 100)
        
        elif action == Actions.CORE_MOVE_RIGHT:
            player.core_move_right(self._time_between_frame)
            self._player_thruster_particle_effect[player].emit(player.get_coor(), (-0.03, 0), 0.02, 0.1, 5, 100)

    def __draw_blocks(self, zero_vector:tuple, unit_size:int) -> None:
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
                self.build_players()


    def __battle_key_events(self):
        # key events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    self._running = False

            if event.type == pygame.KEYDOWN:
                for key in KeyGroups.ThrusterKeys:
                    if event.key == key:
                        Sounds.THRUSTER_BURN.play()

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
