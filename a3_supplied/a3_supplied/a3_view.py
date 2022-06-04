from a3 import Inventory, Tile, Item, Level, Model, Maze
from a3_support import AbstractGrid
import tkinter as tk
from tkinter import Label, ttk, messagebox
from typing import *
import constants
from PIL import ImageTk, Image

class LevelView(AbstractGrid):
    """ A view for a level in the game. """
    def __init__(
        self,
        master: Union[tk.Tk, tk.Frame],
        dimensions: tuple[int, int],
        size: tuple[int, int],
        **kwargs
        ) -> None:
        """ Constructs a new LevelView.
        """
        self._dimensions = dimensions
        self._size = size
        super().__init__(master, dimensions, size, **kwargs)

    def changeDimensions(self, dimensions: tuple[int, int]) -> None:
        self._dimensions = dimensions
        
    def draw(self, tiles: list[list[Tile]], items: dict[tuple[int, int], Item],
            player_pos: tuple[int, int]) -> None:
        """ Draws the given tiles and items on the grid.
        
        Parameters:
            tiles: A list of lists of Tile objects.
            items: A dictionary mapping positions to Item objects.
            player_pos: The position of the player.
        """

        for row in range(self._dimensions[0]):
            for col in range(self._dimensions[1]):
                if tiles[row][col].get_id() == constants.WALL:
                    color = constants.TILE_COLOURS[constants.WALL]
                elif tiles[row][col].get_id() == constants.EMPTY:
                    color = constants.TILE_COLOURS[constants.EMPTY]
                elif tiles[row][col].get_id() == constants.DOOR:
                    color = constants.TILE_COLOURS[constants.DOOR]
                else:
                    color = constants.TILE_COLOURS[constants.LAVA]
                self.create_rectangle(
                    col * (self._size[1])/self._dimensions[1],
                    row * (self._size[0])/self._dimensions[0], 
                    (col + 1) * (self._size[1])/self._dimensions[1], 
                    (row + 1) * (self._size[0])/self._dimensions[0], 
                    fill = color
                )

        self.create_oval(
            player_pos[1] * (self._size[1])/self._dimensions[1],
            player_pos[0] * (self._size[0])/self._dimensions[0],
            (player_pos[1] + 1) * (self._size[1])/self._dimensions[1],
            (player_pos[0] + 1) * (self._size[0])/self._dimensions[0],
            fill=constants.ENTITY_COLOURS[constants.PLAYER],
            width = 1
        )

        self.create_text(
            (player_pos[1] + 0.5) * (self._size[1])/self._dimensions[1],
            (player_pos[0] + 0.5) * (self._size[0])/self._dimensions[0],
            text = constants.PLAYER,
            font = constants.TEXT_FONT,
        )

        for key, value in items.items():
            if value.get_id() == constants.COIN:
                color = constants.ENTITY_COLOURS[constants.COIN]
            elif value.get_id() == constants.POTION:
                color = constants.ENTITY_COLOURS[constants.POTION]
            elif value.get_id() == constants.HONEY:
                color = constants.ENTITY_COLOURS[constants.HONEY]
            elif value.get_id() == constants.APPLE:
                color = constants.ENTITY_COLOURS[constants.APPLE]
            elif value.get_id() == constants.WATER:
                color = constants.ENTITY_COLOURS[constants.WATER]
            elif value.get_id() == constants.CANDY:
                color = constants.ENTITY_COLOURS[constants.CANDY]
            else:
                color = constants.ENTITY_COLOURS[constants.LAVA_SHOES]
            self.create_oval(
                key[1] * (self._size[1])/self._dimensions[1],
                key[0] * (self._size[0])/self._dimensions[0],
                (key[1] + 1) * (self._size[1])/self._dimensions[1],
                (key[0] + 1) * (self._size[0])/self._dimensions[0],
                fill = color
            )
            self.create_text(
                (key[1] + 0.5) * (self._size[1])/self._dimensions[1],
                (key[0] + 0.5) * (self._size[0])/self._dimensions[0],
                text = value.get_id(),
                font = constants.TEXT_FONT,
            )
        
class Title(AbstractGrid):
    '''Display the title of game'''
    def __init__(
        self, 
        master: Union[tk.Tk, tk.Frame], 
        size: tuple[int, int], **kwargs
        ) -> None:
        super().__init__(master, (1, 1), size, **kwargs)
        self._size = size
        
    def draw(self) -> None:
        self.create_text(
            0.5 * self._size[0],
            0.5 * self._size[1],
            text = "MazeRunner",
            font = constants.BANNER_FONT,
        )

class StatsView(AbstractGrid):
    """ A view for the player's stats. """
    def __init__(
        self,
        master: Union[tk.Tk, tk.Frame],
        width: int,
        **kwargs
        ) -> None:
        """ Constructs a new StatsView.
        """
        self._width = width
        super().__init__(master, (1, 3), (width, constants.STATS_HEIGHT), **kwargs)
        
    def draw_stats(self, player_stats: tuple[int, int, int]) -> None:
        """ Draws the given player stats on the grid.
        Parameters:
            player_stats: A tuple of (health, attack, defense)
        """
        self.create_text(
            self._width/8,
            constants.STATS_HEIGHT/4,
            text = "HP",
            font = constants.TEXT_FONT,
        )
        self.create_text(
            self._width/8,
            3 * constants.STATS_HEIGHT/4,
            text = str(player_stats[0]),
            font = constants.TEXT_FONT,
        )
        self.create_text(
            3 * self._width/8,
            constants.STATS_HEIGHT/4,
            text = "Hunger",
            font = constants.TEXT_FONT,
        )
        self.create_text(
            3 * self._width/8,
            3 * constants.STATS_HEIGHT/4,
            text = str(player_stats[1]),
            font = constants.TEXT_FONT,
        )
        self.create_text(
            5 * self._width/8,
            constants.STATS_HEIGHT/4,
            text = "Thirst",
            font = constants.TEXT_FONT,
        )
        self.create_text(
            5 * self._width/8,
            3 * constants.STATS_HEIGHT/4,
            text = str(player_stats[2]),
            font = constants.TEXT_FONT,
        )

    def draw_coins(self, num_coins: int) -> None:
        """ Draws the given number of coins on the grid.
        
        Parameters:
            num_coins: The number of coins to draw.
        """
        self.create_text(
            7 * self._width/8,
            constants.STATS_HEIGHT/4,
            text = "Coins",
            font = constants.TEXT_FONT,
        )
        self.create_text(
            7 * self._width/8,
            3 * constants.STATS_HEIGHT/4,
            text = str(num_coins),
            font = constants.TEXT_FONT,
        )

class InventoryView(AbstractGrid):
    """ A view for the player's inventory. """
    def __init__(
        self,
        master: Union[tk.Tk, tk.Frame],
        **kwargs
        ) -> None:
        """ Constructs a new InventoryView.
        """
        super().__init__(master, (1, 1), (constants.INVENTORY_WIDTH, constants.MAZE_HEIGHT), **kwargs)
        self.ht = 15
        
    def set_click_callback(
        self,
        callback: Callable[[str], None]
        ) -> None:
        """ Sets the callback to be called when an item is clicked.
        
        Parameters:
            callback: The callback to be called.
        """
        pass

    def clear(self) -> None:
        """ Clears the grid.
        """
        super().clear()
        self.ht = 15

    def _draw_item(self, name: str, num: int, colour: str) -> None:
        self.ht += 50
        button = tk.Button(
            self,
            font = constants.TEXT_FONT,
            bg = colour,
            command=lambda: self.set_click_callback(name),
            text = name + ": " + str(num),
            # width = constants.INVENTORY_WIDTH // 2,
        )
        button.place(x=0 , y=self.ht)

    def draw_inventory(self, inventory: Inventory) -> None:
        """ Draws the given inventory on the grid.
        
        Parameters:
            inventory: The inventory to draw.
        """
        self.create_text(constants.INVENTORY_WIDTH / 2, self.ht, text = "Inventory", font = constants.HEADING_FONT) 
        dic = inventory.get_items()
        for key, value in dic.items():
            # print(key, value)
            if key == 'Coin':
                colour = constants.ENTITY_COLOURS[constants.COIN]
            elif key == 'Water':
                colour = constants.ENTITY_COLOURS[constants.WATER]
            elif key == 'Potion':
                colour = constants.ENTITY_COLOURS[constants.POTION]
            elif key == 'Apple':
                colour = constants.ENTITY_COLOURS[constants.APPLE]
            else:
                colour = constants.ENTITY_COLOURS[constants.HONEY]
            self._draw_item(key, len(value), colour)

class ImageLevelView(LevelView):
    """ A view for the player's inventory. """
    def __init__(
        self,
        master: Union[tk.Tk, tk.Frame],
        dimensions: tuple[int, int],
        size: tuple[int, int],
        **kwargs
        ) -> None:
        """ Constructs a new LevelView.
        """
        self._dimensions = dimensions
        self._size = size
        super().__init__(master, dimensions, size, **kwargs)

    def draw(self, tiles: list[list[Tile]], items: dict[tuple[int, int], Item],
            player_pos: tuple[int, int]) -> None:
        """ Draws the given tiles and items on the grid.
        
        Parameters:
            tiles: A list of lists of Tile objects.
            items: A dictionary mapping positions to Item objects.
            player_pos: The position of the player.
        """
        for row in range(self._dimensions[0]):
            for col in range(self._dimensions[1]):
                image = Image.open('images/' + constants.TILE_IMAGES[tiles[row][col].get_id()])
                img = ImageTk.PhotoImage(image=image.resize((self._size[0] // self._dimensions[1], self._size[1] // self._dimensions[0])))
                label = Label(self, image=img)
                label.image = img
                label.place(x=col * self._size[0] // self._dimensions[1], y=row * self._size[1] // self._dimensions[0])

        image = Image.open('images/' + constants.ENTITY_IMAGES[constants.PLAYER])
        img = ImageTk.PhotoImage(image=image.resize((self._size[0] // self._dimensions[1], self._size[1] // self._dimensions[0])))
        label = Label(self, image=img)
        label.image = img
        label.place(x=player_pos[1] * self._size[0] // self._dimensions[1], y=player_pos[0] * self._size[1] // self._dimensions[0])

        for key, value in items.items():
            image = Image.open('images/' + constants.ENTITY_IMAGES[value.get_id()])
            img = ImageTk.PhotoImage(image=image.resize((self._size[0] // self._dimensions[1], self._size[1] // self._dimensions[0])))
            label = Label(self, image=img)
            label.image = img
            label.place(x=key[1] * self._size[0] // self._dimensions[1], y=key[0] * self._size[1] // self._dimensions[0])

class GraphicalInterface(AbstractGrid):
    """ A graphical interface for the game. """
    def __init__(
        self,
        master: tk.Tk,
        dimensions: tuple[int, int],
        ) -> None:
        """ Constructs a new GraphicalInterface.
        """
        super().__init__(master, (1, 1), (constants.MAZE_WIDTH + constants.INVENTORY_WIDTH, constants.MAZE_HEIGHT + 2 * constants.STATS_HEIGHT))
        self.grid()
        self.should_stop = False
        # title instance
        self.title = Title(self, (constants.MAZE_WIDTH + constants.INVENTORY_WIDTH, constants.STATS_HEIGHT))
        self.title.place(x=0, y=0)
        self.title.config(bg=constants.THEME_COLOUR)
        self.title.draw()
        # inventory instance
        self.inventoryView = InventoryView(self)
        self.inventoryView.place(x=constants.MAZE_WIDTH, y=constants.STATS_HEIGHT)
        # stateView instance
        self.stateView = StatsView(self, constants.MAZE_WIDTH + constants.INVENTORY_WIDTH)
        self.stateView.config(bg=constants.THEME_COLOUR)
        self.stateView.place(x=0, y=constants.MAZE_HEIGHT+constants.STATS_HEIGHT)
        # level instance
        if constants.TASK == 1:
            self.levelView = LevelView(self, dimensions, (constants.MAZE_WIDTH, constants.MAZE_HEIGHT))
            self.levelView.place(x=0, y=constants.STATS_HEIGHT)
        else:
            self.levelView = ImageLevelView(self, dimensions, (constants.MAZE_WIDTH, constants.MAZE_HEIGHT))
            self.levelView.place(x=0, y=constants.STATS_HEIGHT)

        
    def create_interface(
        self, 
        maze: Maze,
        inventory: Inventory,
        player_stats: tuple[int, int, int],
        items: dict[str, list[str]],
        player_position: tuple[int, int],
        ) -> None:
        """ Creates the interface for the game.
        
        Parameters:
            dimensions: The dimensions of the level.
        """
        if not self.should_stop:
            # inventory view
            self.inventoryView.clear()
            self.inventoryView.draw_inventory(inventory)
            # stats view
            self.stateView.clear()
            self.stateView.draw_stats(player_stats)
            self.stateView.draw_coins(len([item.get_id() == constants.COIN for item in items.values()]))
            # level view
            self.levelView.set_dimensions(maze.get_dimensions())
            self.levelView.clear()
            self.levelView.draw(maze.get_tiles(), items,
                player_position)


    def clear_all(self) -> None:
        """ Clears all of the interface. """
        super().clear()

    def on_closing(self) -> None:
        """ Called when the window is closing. """
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.should_stop = True
            self.destroy()

    def set_maze_dimensions(self, dimensions: tuple[int, int]) -> None:
        """ Sets the dimensions of the maze.
        
        Parameters:
            dimensions: The dimensions of the maze.
        """
        self.levelView.changeDimensions(dimensions)

    def bind_keypress(self, command: Callable[[tk.Event], None]) -> None:
        """ Binds a keypress to the given command.
        
        Parameters:
            command: The command to be called.
        """
        self.master.bind("<Key>", command)

    def set_inventory_callback(self, callback: Callable[[str], None]) -> None:
        """ Sets the callback to be called when an item is clicked.
        
        Parameters:
            callback: The callback to be called.
        """
        self.inventoryView.set_click_callback(callback)

    def draw_inventory(self, inventory: Inventory) -> None:
        """ Draws the given inventory on the grid.
        
        Parameters:
            inventory: The inventory to draw.
        """
        self.inventoryView.draw_inventory(inventory)

    def draw(
        self,
        maze: Maze,
        items: dict[tuple[int, int], Item],
        player_position: tuple[int, int],
        inventory: Inventory,
        player_stats: tuple[int, int, int]
    ) -> None:
        """ Draws the given maze on the grid.
        
        Parameters:
            maze: The maze to draw.
            items: The items to draw.
            player_position: The position of the player.
            inventory: The inventory to draw.
            player_stats: The stats of the player.
        """
        self.create_interface(maze, inventory, player_stats, items, player_position)

    def _draw_inventory(self, inventory: Inventory) -> None:
        self.inventoryView.draw_inventory(inventory)

    def _draw_level(self, maze: Maze, items: dict[tuple[int, int], Item],
                    player_position: tuple[int, int]) -> None:
        self.levelView.draw(maze, items, player_position)

    def _draw_player_stats(self, player_stats: tuple[int, int, int]) -> None:
        self.stateView.draw_stats(player_stats)