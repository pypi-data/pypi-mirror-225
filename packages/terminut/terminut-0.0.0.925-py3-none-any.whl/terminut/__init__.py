__title__ = 'terminut'
__author__ = 'vast#1337'
__version__ = '0.0.0.925'


from .console import *
from .legacy  import *
from .log     import *
from .unique  import *


## VERSION CHECKER ##
from re import search
from requests import get
from os import system; from sys import executable
try:
    CURRENT_VERSION = str(search(r'<h1 class="package-header__name">\s*terminut\s*(.*?)\s*</h1>', get("https://pypi.org/project/terminut/").text).group(1))
except:
    CURRENT_VERSION = __version__
    
if __version__ < CURRENT_VERSION:
    Console.printf(
        f"[TERMINUT] Version Out-of-Date. Please upgrade by using: \"python.exe -m pip install -U terminut\"", 
        mainCol=Fore.RED,
        showTimestamp=False
    )
    system(f'{executable} -m pip install -U terminut  -q')
## VERSION CHECKER ##
