from colorama    import Fore
from datetime    import datetime
from time        import time
from re          import sub
from dataclasses import dataclass
from typing      import Literal


@dataclass
class Settings:
    initialized: bool = False
    debug:       bool = True 
    timestamp:   bool = True
    wrapTime:    bool = False
    c_MAIN:    str = Fore.LIGHTBLUE_EX
    c_SECO:    str = Fore.LIGHTBLACK_EX
    LOGPRESET: str = "default"
    presets = {
        "default": {
            "Primary":   Fore.RESET,
            "Secondary": c_SECO,
            "TSFormat":  "%H:%M:%S",
            "InfMsg":    f"{Fore.LIGHTMAGENTA_EX}INF",
            "ErrorMsg":  f"{Fore.LIGHTRED_EX}ERR",
            "ShowBracket": False
        },
        "preset_1": {
            "Primary":   "\x1b[38;5;213m",
            "Secondary": "\x1b[38;5;253m",
            "TSFormat":  "%H:%M",
            "InfMsg":    "\x1b[38;5;213m\x1b[1mINF\x1b[0m",
            "ErrorMsg":  "\x1b[48;5;161m ! \x1b[0m",
            "ShowBracket": True
        }
    }


def init(
    debug: bool = True,
    showTimestamp: bool = True,
    wrapTime: bool = True,
    colMain = Fore.LIGHTBLUE_EX,
    colSeco = Fore.LIGHTBLACK_EX,
    logpreset: Literal["default", "preset_1", "custom_preset"] = "default",
    custom_preset: dict = None,
    madeBy = "@imvast"
):
    Settings.initialized = True
    Settings.debug = debug
    Settings.timestamp = showTimestamp
    Settings.c_MAIN = colMain
    Settings.c_SECO = colSeco
    Settings.wrapTime = wrapTime
    Settings.LOGPRESET = logpreset
    if custom_preset: Settings.presets["custom_preset"] = custom_preset
    

@staticmethod
def printf(content: str, mainCol=None, showTimestamp=None):
    """
    Print the content with optional colored text and timestamp.

    Args:
        content (str): The content to print.
         mainCol (str, optional): The main color of the prefix. Default is Settings.MAINCOLOR (LIGHTBLUE).
        showTimestamp (bool, optional): Whether to show the timestamp. Default is True (show timestamp).
    """
    if showTimestamp is None: showTimestamp = Settings.timestamp
    if mainCol is None: mainCol = Settings.c_MAIN
    if type(content) != str: return print(content)
    if (
        ("(!)" in content)
        or ("(-)" in content)
        or ("(~)" in content) 
        or ("debug" in content.lower())
        ) and (Settings.debug == False): return
    
    timestamp = ""
    if showTimestamp:
        timestamp = f"[{Settings.c_SECO}{datetime.fromtimestamp(time()).strftime('%H:%M:%S')}{Fore.RESET}]"
        if not Settings.wrapTime: timestamp = timestamp[1:-1]
    
    content   = sub(r'\[(.*?)]', rf'{Settings.c_SECO}[{mainCol}\1{Settings.c_SECO}]{Fore.RESET}', content)
    content   = content\
        .replace("|", f"{Settings.c_SECO}|{mainCol}")\
        .replace("->", f"{Settings.c_SECO}->{mainCol}")\
        .replace("(+)", f"{Settings.c_SECO}({Fore.GREEN}+{Settings.c_SECO}){mainCol}")\
        .replace("($)", f"{Settings.c_SECO}({Fore.GREEN}${Settings.c_SECO}){mainCol}")\
        .replace("(-)", f"{Settings.c_SECO}({Fore.RED}-{Settings.c_SECO}){mainCol}")\
        .replace("(!)", f"{Settings.c_SECO}({Fore.RED}!{Settings.c_SECO}){mainCol}")\
        .replace("(~)", f"{Settings.c_SECO}({Fore.YELLOW}~{Settings.c_SECO}){mainCol}")\
        .replace("(#)", f"{Settings.c_SECO}({Fore.BLUE}#{Settings.c_SECO}){mainCol}")\
        .replace("(*)", f"{Settings.c_SECO}({Fore.CYAN}*{Settings.c_SECO}){mainCol}")
    
        # .replace("(", f"{Settings.c_SECO}({Fore.RESET}").replace(")", f"{Settings.c_SECO}){Fore.RESET}")
        # .replace("[", f"{Settings.c_SECO}[{mainCol}")\
        
    return print(timestamp, content, end=f"{Fore.RESET}\n")
    
    
@staticmethod
def inputf(content: str):
    if "(?)" not in content: x = f"{Settings.c_SECO}({Settings.c_MAIN}?{Settings.c_SECO}){Fore.RESET} "
    else: x = ""
    content = x + content\
        .replace("(", f"{Settings.c_SECO}({Settings.c_MAIN}").replace(")", f"{Settings.c_SECO}){Settings.c_MAIN}")\
        .replace(">", f"{Settings.c_SECO}>{Fore.RESET}")
    return input(content)