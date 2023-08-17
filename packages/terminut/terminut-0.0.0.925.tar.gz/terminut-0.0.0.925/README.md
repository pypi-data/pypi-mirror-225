# Terminut.
<img src="https://img.shields.io/pypi/v/terminut?style=for-the-badge&logo=python">
<img alt="followers" src="https://img.shields.io/github/followers/imvast?color=f429ff&style=for-the-badge&logo=github&label=Follow"/>

```less
                > Custom Console Going To Be Used For My Projects
                    And Available To Anyone Else Who Wants To Use <
```

---

### Installation
```
! package NOT FULLY available for non-personal use !
~ use at the knowledge of knowing it may be buggy ~

pip install terminut
```

### Usage
```py
# default shit if u want to only import for ease - auto switches #

from terminut import printf as print, inputf as input, init

init(debug=False)

print("[DEBUG] Should NOT Show")
print("(~) Should NOT Show")
print("[INFO] Should Show")
print("(*) Should Show")

# --------------------------------------------------------- #
# log format: [21:14:38] INF > test

from terminut import log

log.info(
    "info",
    sep=">" # separator OPTIONAL
)
log.error("error")
log.fatal("fatal")
log.success("success")

# --------------------------------------------------------- #
# this is for custom cool stuff as seen here: 
# https://cdn.discordapp.com/attachments/1099515953223569420/1105295220414885998/2023-05-08_20-46-22.mp4

import time
from terminut import BetaConsole

c = BetaConsole(speed=2)

while True:
    try:
        timestamp = c.getTimestamp()
        c.alphaPrint("[INF]", f"[{timestamp}] made by vast :D", increment=False)
        time.sleep(0.001)
    except KeyboardInterrupt: exit(0)
```

---

## * [imvast@discord](https://discord.com/users/1118654675898617891) | [imvast@github](https://github.com/imvast) | [vast.sh](https://vast.sh) *