import pygame;
import os;
import platform;
from enum import Enum;
from typing import List;

class Obstacle(Enum):
    EMPTY = 1
    DOT = 2
    WALL = 3
    GHOST = 4
    PILL = 5
    PACMAN = 6
    VOID = 7


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    DEAD = 5


class Map:
    __MAP_HEIGHT = 20;
    __MAP_WIDTH = 20;


    def __init__(self, map_name : str, game) -> None:
        self.__game = game;
        self.__board_model = [['' for x in range(Map.__MAP_HEIGHT)] for y in range(Map.__MAP_WIDTH)]
        self.__board_view = [[pygame.Surface((32,32), pygame.SRCALPHA, 32) for x in range(Map.__MAP_HEIGHT)] for y in range(Map.__MAP_WIDTH)]
        pygame.font.init()
        self.__font = pygame.font.Font(pygame.font.get_default_font(), 24)
        self.__dot_count = 0
        self.__player = Pacman()
        self.__ghost = None;
        self.__build_map_model(map_name)


    def __build_map_model(self, map_name : str) -> None:
        map_data = self.__read_map(map_name)
        if(platform.system() == "Windows"):
            self.__difficulty = map_data[0][3:];
        else:
            self.__difficulty = map_data[0];
        self.__total_moves = int(map_data[1]);
        for i in range(0, len(map_data) - 2):
            chars = list(map_data[i + 2])
            for j in range(0, len(chars)):
                match chars[j]:
                    case '-':
                        self.__board_model[j][i] = Obstacle.EMPTY
                    case '.':
                        self.__dot_count += 1
                        self.__board_model[j][i] = Obstacle.DOT
                    case 'g':
                        self.__board_model[j][i] = Obstacle.GHOST
                        self.__ghost = Ghost()
                        self.__ghost.set_map_index(j, i)
                        self.__ghost.sprite = load_image("ghost.png");
                    case 'x':
                        self.__board_model[j][i] = Obstacle.PILL
                    case 'p':
                        self.__board_model[j][i] = Obstacle.PACMAN
                        self.__player.set_map_index(j, i)
                        self.__player.sprite = load_image("PacmanUP.png");
                    case 'w':
                        self.__board_model[j][i]  = Obstacle.WALL

                self.__build_map_view(i, j)  
    

    def __build_map_view(self, column : int, row : int) -> None:
        obstacleName = self.__board_model[row][column].name;
        if obstacleName.upper() != "PACMAN" and obstacleName.upper() != "GHOST" and obstacleName.upper() != "EMPTY":
            self.__board_view[row][column] = load_image(obstacleName.lower() + ".png")
        

    def draw_map(self, screen : pygame.Surface) -> None:
        pygame.draw.rect(screen, (255,255,255), rect=pygame.Rect(0, 0, 784, 50))
        screen.blit(self.__font.render(self.__game._PacmanGame__message, True, (0,0,0)), (8, 8))

        for i in range(0, self.__MAP_WIDTH):
            for j in range(0, self.__MAP_HEIGHT):
                if self.__board_model[j][i] != Obstacle.EMPTY and self.__board_model[j][i] != Obstacle.PACMAN and self.__board_model[j][i] != Obstacle.GHOST:
                    screen.blit(self.__board_view[j][i], [54 + (j * 32), 54 + (i * 32)])

        if(self.__player is not None):
            screen.blit(self.__player.sprite, self.__player.position)
        if(self.__ghost is not None):
            screen.blit(self.__ghost.sprite, self.__ghost.position)

        pygame.draw.rect(screen, (255,255,255), rect=pygame.Rect(0, 734, 784, 50))
        screen.blit(self.__font.render("difficulty:" + str(self.__difficulty) + ", player position [" + str(self.__player.map_index[0]) + ", " + str(self.__player.map_index[1]) +"], steps:" + str(self.__game._PacmanGame__moves_taken) + "/" + str(self.__total_moves), True, (0,0,0)), (8, 748))


    def update_pacman(self, delta_movement, new_direction : Direction) -> None:
        if delta_movement != [0,0]:
            new_position = [0, 0]
            new_position[0] = self.__player.map_index[0] + delta_movement[0];
            new_position[1] = self.__player.map_index[1] + delta_movement[1];
            if new_position[0] >= self.__MAP_WIDTH or new_position[1] >= self.__MAP_HEIGHT or new_position[0] < 0 or new_position[1] < 0:
                raise Exception("Index was outside the bounds of the array.")
            if self.get_obstacle_at_coords(new_position[0], new_position[1]) == Obstacle.DOT:
                self.__dot_count -= 1
            elif self.get_obstacle_at_coords(new_position[0], new_position[1]) == Obstacle.PILL:
                self.__ghost._Ghost__toggle_edible_state()
            
            if self.get_obstacle_at_coords(new_position[0], new_position[1]) != Obstacle.WALL:
                self.__board_model[self.__player.map_index[0]][self.__player.map_index[1]] = Obstacle.EMPTY
                self.__player.set_map_index(new_position[0], new_position[1])
                self.__board_model[self.__player.map_index[0]][self.__player.map_index[1]] = Obstacle.PACMAN

                self.update_ghost()

            self.__board_view[new_position[0]][new_position[1]] = None

        if self.__player.direction != Direction.DEAD:
            self.__player.set_direction(new_direction)

    
    def update_ghost(self):
        if self.__ghost is not None:
            if self.__ghost.is_edible and self.__player.map_index == self.__ghost.map_index:
                self.__ghost = None
            
            if self.__ghost is not None:
                delta_movement = [0, 0]
                if self.__player.map_index[1] < self.__ghost.map_index[1]:
                    delta_movement[1] = -1
                elif self.__player.map_index[0] < self.__ghost.map_index[0]:
                    delta_movement[0] = -1
                elif self.__player.map_index[1] > self.__ghost.map_index[1]:
                    delta_movement[1] = 1
                elif self.__player.map_index[0] > self.__ghost.map_index[0]:
                    delta_movement[0] = 1

                self.__ghost.set_map_index(self.__ghost.map_index[0] + delta_movement[0], self.__ghost.map_index[1] + delta_movement[1])

                if self.__ghost.is_edible == False and self.__player.map_index == self.__ghost.map_index:
                    self.__player.set_direction(Direction.DEAD)
                    self.__ghost.set_map_index(self.__ghost.map_index[0] - delta_movement[0], self.__ghost.map_index[1] - delta_movement[1])
                

    def get_obstacle_at_coords(self, column : int, row : int) -> Obstacle:
        if row < 0 or column < 0 or row >= self.__MAP_HEIGHT or column >= self.__MAP_WIDTH:
            return Obstacle.VOID
        else:
            return self.__board_model[column][row]


    def __read_map(self, map_name : str) -> List[str]:
        lines = []
        with open(get_map_path(map_name + '.map')) as f:
            lines = f.read().splitlines()
        return lines;


    def get_pacman(self) -> 'Pacman':
        return self.__player;


    def get_pacman_direction(self) -> Direction:
        return self.__player.direction;


def load_image(package_path: str) -> pygame.Surface:
        return pygame.image.load(os.path.dirname(__file__) + "/images/" + package_path)


def get_map_path(package_path: str) -> List[str]:
    return os.path.dirname(__file__) + "/maps/" + package_path


class Pacman:
    def __init__(self) -> None:
        self.map_index = [0, 0]
        self.position = []
        self.sprite_list = []
        self.create_sprite_list()
        self.set_direction(Direction.UP)
        self.sprite = pygame.Surface((32,32));


    def set_map_index(self, row : int, column : int) -> None:
        self.map_index = [row, column]
        self.position = [54 + (row * 32), 54 + (column * 32)]


    def create_sprite_list(self):
        for i in range(5):
            self.sprite_list.append(load_image("Pacman" + Direction(i + 1).name + ".png"))
            #self.sprite_list.append(pygame.image.load("images/Pacman" + Direction(i + 1).name + ".png"))
        self.sprite = self.sprite_list[0]


    def set_direction(self, new_direction : Direction):
        self.direction = new_direction
        self.sprite = self.sprite_list[new_direction.value - 1]


class Ghost:
    def __init__(self) -> None:
        self.is_edible = False;
        self.map_index = [0, 0];
        self.position = [];
        self.sprite = pygame.Surface((32,32));


    def set_map_index(self, row : int, column : int) -> None:
        self.map_index = [row, column]
        self.position = [54 + (row * 32), 54 + (column * 32)]


    def toggle_edible_state(self) -> None:
        self.is_edible = not self.is_edible

        if self.is_edible:
            self.sprite = load_image("eatable_ghost.png")
        else:
            self.sprite = load_image("ghost.png")

    
