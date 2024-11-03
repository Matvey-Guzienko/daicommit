from colorama import Fore
from typing import Literal

from pick import pick

def into(text: str):
    return input(Fore.GREEN + "> " + Fore.RESET + f"{text}: ")

def outro(text: str, type: Literal["red", "green", "blue", "yellow"]):
    prefix_color = Fore.LIGHTRED_EX if type == 'red' else Fore.LIGHTGREEN_EX if type == 'green' else Fore.LIGHTBLUE_EX if type == 'blue' else Fore.LIGHTYELLOW_EX if type == 'yellow' else Fore.RESET
    print(prefix_color + "> " + Fore.RESET + text)

def menu(title: str, options: list):
    return pick(options, title, indicator=">")[0]
