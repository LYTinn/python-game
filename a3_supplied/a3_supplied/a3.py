import tkinter as tk
from typing import *
from a3_view import *
from a3_support import *
from constants import *
from a2_solution import *

# Write your classes here

class GraphicalMazeRunner(MazeRunner):
    def __init__(self, game_file: str, view: UserInterface) -> None:
        super().__init__(game_file, view)
        self._view = view
    def _handle_keypress(self, e: tk.Event) -> None:
        key = e.keysym
        if key == 'Up':
            self.move(UP)
        elif key == 'Down':
            self.move(DOWN)
        elif key == 'Left':
            self.move(LEFT)
        elif key == 'Right':
            self.move(RIGHT)
        elif key == 'q':
            self.quit()
        elif key == 'r':
            self.restart()
        elif key == 's':
            self.save()
        elif key == 'l':
            self.load()
        else:
            print('Unrecognized key:', key)

    def _apply_item(self, item_name: str) -> None:
        if item_name == 'apple':
            self.apply_apple()
        elif item_name == 'honey':
            self.apply_honey()
        elif item_name == 'water':
            self.apply_water()
        elif item_name == 'potion':
            self.apply_potion()
        else:
            print('Unrecognized item:', item_name)

    def play(self) -> None:
        self._view.draw_game(self.game)
        self._view.bind('<KeyPress>', self._handle_keypress)
        self._view.mainloop()


def main():
    # Write your main function code here
    game_file = input('Enter game file: ')
    levels = load_game(game_file)
    view = GraphicalInterface(tk.Tk(), levels[0].get_maze().get_dimensions())
    game = MazeRunner(game_file, view)
    game.play()

if __name__ == '__main__':
    main()
