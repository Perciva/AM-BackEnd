
from colorama import Fore, init
magenta = "\033[0;35m"
black = "\033[0;30m"
red = "\033[0;31m"
green = "\033[0;32m"
yellow = "\033[0;33m"
blue = "\033[0;34m"
cyan = "\033[0;36m"
white = "\033[0;37m"
default = "\033[0;38m"
init(convert=True)
def reset():
    print(default, end='')

def pred(text): 
    print(red + text)
    reset()
def pgreen(text): 
    print(green + text)
    reset()
def pyellow(text): 
    print(yellow + text)
    reset()
def pblue(text): 
    print(blue + text)
    reset()
def pcyan(text): 
    print(cyan + text)
    reset()
def pwhite(text): 
    print(white + text)
    reset()
def pmagenta(text): 
    print(magenta + text)
    reset()
