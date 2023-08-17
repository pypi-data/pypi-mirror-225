from datetime import datetime
from time     import time
from colorama import Fore, init as colinit
from .colors  import *

from .console import Settings


class log:
    def __init__(self) -> None:
        colinit(autoreset=True)

    @staticmethod
    def _get_timestamp():
        scrp = Settings.presets.get(Settings.LOGPRESET, Settings.presets["default"])
        if Settings.timestamp:
            timestamp = (
                (f"{scrp.get('Primary')}[" if scrp.get("ShowBracket") else "")
                + (f"{scrp.get('Secondary')}"
                + f"{datetime.fromtimestamp(time()).strftime(scrp.get('TSFormat'))}")
                + (f"{scrp.get('Primary')}]" if scrp.get("ShowBracket") else "")
                + f"{Fore.RESET}"
                )
        else:
            timestamp = ""
        return timestamp, scrp
    
    @staticmethod
    def success(text: str, sep: str = " "):
        timestamp,_ = log._get_timestamp()
        print(f"{timestamp} {Fore.GREEN}YES {Fore.LIGHTBLACK_EX}{sep}{Fore.RESET}{text}")
        
    @staticmethod
    def info(text: str, sep: str = " "):
        timestamp, scrp = log._get_timestamp()
        print(f"{timestamp} {scrp.get('InfMsg')} {Fore.LIGHTBLACK_EX}{sep}{Fore.RESET}{text}")

    @staticmethod
    def error(text: str, sep: str = " "):
        timestamp, scrp = log._get_timestamp()
        print(f"{timestamp} {scrp.get('ErrorMsg')} {Fore.LIGHTBLACK_EX}{sep}{Fore.RESET}{text}")

    @staticmethod
    def fatal(text: str, sep: str = " "):
        timestamp,_ = log._get_timestamp()
        print(f"{timestamp} {Fore.RED}FTL {Fore.LIGHTBLACK_EX}{sep}{Fore.RESET}{text}")

