from tkinter import simpledialog;
import importlib.resources as pkg_resources;
import time;
import threading, os;
import platform;
import ctypes;
import pygame;

from pycman_dna.map import Map
from pycman_dna.map  import Direction;

class PacmanGame:
    """
    PacmanGame's base constructor method. Performs initial setup.
    """
    __update_rate = 0.25;
    __moves_taken = 0;
    def __init__(self):
        self.__screen = None
        self.__render_surface = None
        self.__game_running = True;
        self.__message = "No message"
        self.__map = None;
        self.__map_name = ""
        self.set_update_rate(250)
        if(platform.system() == "Windows"):
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
        if(platform.system() == "Linux"):
            ctypes


    def __run_game(self) -> None:
        """
        
        """
        pygame.init();
        
        self.__render_surface = pygame.Surface((784, 784))
        if platform.system() == "Windows":
            self.__screen = pygame.display.set_mode([784, 784], pygame.SCALED | pygame.RESIZABLE)
        else:
            self.__screen = pygame.display.set_mode([400, 400], pygame.SCALED)
        pygame.display.set_icon(pygame.image.load(os.path.dirname(__file__) + "/images/icon.png"))
        pygame.display.set_caption("Pycman - " + "\"" +self.__map_name + "\"")

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.__game_running = False
                    os._exit(1)
                if event.type == pygame.VIDEORESIZE:
                    self.__screen = pygame.display.set_mode([event.w, event.h], pygame.SCALED | pygame.RESIZABLE)
            # Fill the background with black
            self.__screen.fill((0, 0, 0))
            self.__render_surface.fill((0, 0, 0))
            
            self.__map.draw_map(self.__render_surface);
            self.__screen.blit(pygame.transform.smoothscale(self.__render_surface, self.__screen.get_size()), (0,0))
            
            # Flip the display
            pygame.display.flip()
        

    def __check_end_conditions(self):
        if self.__map._Map__dot_count <= 0:
            self.__game_running = False
            self.send_message("All dots collected - well done!")
        elif self.__moves_taken >= self.__map._Map__total_moves:
            self.__game_running = False
            self.send_message("No moves remaining. Please try again.")
            self.__map.update_pacman([0,0], Direction.DEAD)
        elif self.__map.get_pacman_direction() == Direction.DEAD:
            self.__game_running = False
            self.send_message("Pacman has been caught. Please try again.")


    def set_map(self, map_name : str) -> None:
        """
        Sets the game map that Pacman will travel around, based on the map name passed in.
        :param map_name: The name of a built-in game map.
        """
        self.__map_name = map_name
        self.__map = Map(map_name.lower(), self)
        pass;


    def show_game(self) ->None:
        """
        Brings up the game window containing the chosen game map.
        *Please ensure set_map() has been called first.*
        """
        if self.__map is not None:
            self.__thread = threading.Thread(target=PacmanGame.__run_game, args=[self]);
            self.__thread.start();

            time.sleep(1)
        else:
            print("MapError: Map not set. Please set with set_map() method first.")


    def move(self) -> None:
        """
        Moves Pacman one space in the direction he is facing. Counts as a move.
        """
        if(self.__game_running):
            delta_movement = [0, 0]
            match self.__map.get_pacman_direction():
                case Direction.UP:
                    delta_movement[1] = -1
                case Direction.DOWN:
                    delta_movement[1] = 1
                case Direction.LEFT:
                    delta_movement[0] = -1
                case Direction.RIGHT:
                    delta_movement[0] = 1

            self.__map.update_pacman(delta_movement, self.__map.get_pacman_direction())
            PacmanGame.__moves_taken += 1;

            self.__check_end_conditions()
            time.sleep(PacmanGame.__update_rate);


    def turn_right(self) -> None:
        """
        Turns Pacman 90 degrees to the right. Does not count as a move.
        """
        if self.__game_running:
            new_direction = Direction.UP
            match self.__map.get_pacman_direction():
                case Direction.UP:
                    new_direction = Direction.RIGHT
                case Direction.DOWN:
                    new_direction = Direction.LEFT
                case Direction.LEFT:
                    new_direction = Direction.UP
                case Direction.RIGHT:
                    new_direction = Direction.DOWN
            self.__map.update_pacman([0,0], new_direction)
            time.sleep(PacmanGame.__update_rate);

    def turn_left(self) -> None:
        """
        Turns Pacman 90 degrees to the left. Does not count as a move.
        """
        if self.__game_running:
            new_direction = Direction.UP
            match self.__map.get_pacman_direction():
                case Direction.UP:
                    new_direction = Direction.LEFT
                case Direction.DOWN:
                    new_direction = Direction.RIGHT
                case Direction.LEFT:
                    new_direction = Direction.DOWN
                case Direction.RIGHT:
                    new_direction = Direction.UP
            self.__map.update_pacman([0,0], new_direction)
            time.sleep(PacmanGame.__update_rate);

    
    def send_message(self, message : str) -> None:
        """
        Sends a decimal number message to the game window.
        :param message: The text message that should be printed.
        """
        self.__message = message
    

    def is_obstacle_ahead(self, obstacle : str) -> bool:
        """
        Checks whether or not the requested obstacle is directly in front of Pacman. Takes the current direction of Pacman into account. Possible options are:
        \n - Empty
        \n - Dot
        \n - Wall
        \n - Pill
        \n - Void
        \n - Ghost\n
        :param obstacle: The name of an obstacle to look for. Parameter is case insensitive.
        :return: A boolean value (true/false) based on whether or not the requested obstacle was found.
        """
        return obstacle.lower() == self.get_obstacle_ahead().lower()


    def get_obstacle_ahead(self) -> str:
        """
        Returns the name of the obstacle directly in front of Pacman. Takes the current direction of Pacman into account.
        :return: A string containing the name of the obstacle directly ahead of Pacman.
        """
        player_pos = self.__map._Map__player.map_index
        match self.__map._Map__player.direction:
            case Direction.UP:
                return self.__map.get_obstacle_at_coords(player_pos[0], player_pos[1] - 1).name
            case Direction.DOWN:
                return self.__map.get_obstacle_at_coords(player_pos[0], player_pos[1] + 1).name
            case Direction.LEFT:
                return self.__map.get_obstacle_at_coords(player_pos[0] - 1, player_pos[1]).name
            case Direction.RIGHT:
                return self.__map.get_obstacle_at_coords(player_pos[0] + 1, player_pos[1]).name
            
        return self.__map.get_obstacle_at_coords(player_pos[0], player_pos[1]).name


    def set_update_rate(self, update_rate : int) -> None:
        """
        Sets the delay between each update of the game. A lower number results in a faster update rate. 
        \nValues are automatically clamped between 75 and 1000 milliseconds.
        :param update_rate: The amount of time, in milliseconds, to wait between updates.
        """
        if update_rate < 75:
            update_rate = 75
        elif update_rate > 1000:
            update_rate = 1000

        PacmanGame.__update_rate = update_rate * 0.001


    def get_text_from_user(self, prompt: str) -> str:
        """
        Opens an input field for the user to enter some text by keyboard. Pauses the game until complete.
        :param prompt: A message prompt to let the user know what kind of text to enter.
        :return: A string containing the user's entered text.
        """
        text = simpledialog.askstring("Pacman", prompt);
        return text if text is not None else "";


    def get_int_from_user(self, prompt: str) -> int:
        """
        Opens an input field for the user to enter some whole number by keyboard. Pauses the game until complete.
        :param prompt: A message prompt to let the user know what kind of number to enter.
        :return: An integer containing the user's entered number. Returns -1 if something goes wrong.
        """
        num = simpledialog.askinteger("Pacman", prompt);
        return num if num is not None else -1;


    def get_float_from_user(self, prompt: str) -> float:
        """
        Opens an input field for the user to enter some decimal number by keyboard. Pauses the game until complete.
        :param prompt: A message prompt to let the user know what kind of number to enter.
        :return: A double containing the user's entered number. Returns -1 if something goes wrong.
        """
        num = simpledialog.askfloat("Pacman", prompt);
        return num if num is not None else -1;


    def print_map_names(self) -> None:
        """
        Prints out all the names of the built-in game maps available to load.\n
        Uses the standard output stream, which is the terminal for Python projects.
        """
        print("Valid Map Names:\n----------------")
        names = pkg_resources.read_text('pycman_dna', 'map_names.txt').split()
        counter = 0
        for name in names:
            print(str(counter) + ": " + name)
            counter+=1


    def set_window_size(self, width : int, height : int) -> None:
        """
        Changes the size of the window that the PacmanGame is drawn to.\n
        May scale unfavourably if 1:1 ratio is not maintained.\n
        *Windows devices will have their DPI scaling ignored.*
        :param width: The desired width of the window in pixels.
        :param height: The desired height of the window, in pixels.
        """
        resize = pygame.event.Event(pygame.VIDEORESIZE, w=width, h=height)
        pygame.event.post(resize)
        
        #self.__screen = pygame.display.set_mode([width, height], pygame.SCALED)

        
        


    