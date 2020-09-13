# Some useful in-game functions

import os

class GameHelper():

    @staticmethod
    def cls():
        '''Clears console screen.'''
        os.system("cls" if os.name == "nt" else "clear")


if __name__ == "__main__":
    # GameHelper.cls()
    print(GameHelper.cls.__doc__)