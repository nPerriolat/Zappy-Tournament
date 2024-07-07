# AI Documentation

## Table of Contents

0. [Prerequisites](#0-prerequisites)
    1. [Exceptions](#01-exceptions)
    2. [Broadcast protocol](#02-broadcast-protocol)
1. [Commands](#1-commands)
    - [initialize](#initialize)
    - [forward](#forward)
    - [right / left](#right--left)
    - [look](#look)
    - [inventory](#inventory)
    - [broadcast](#broadcast)
    - [connect_nbr](#connect_nbr)
    - [reproduct](#reproduct)
    - [fork](#fork)
    - [eject](#eject)
    - [take](#take)
    - [set_down](#set_down)
    - [incantation](#incantation)
    - [pathfinding](#pathfinding)
    - [gather](#gather)
    - [attack](#attack)
    - [actualize](#actualize)
2. [Strategies](#2-strategies)
    - [worker](#worker)
    - [recruiter](#recruiter)
    - [parrot](#parrot)

## 0. Prerequisites

### 0.1. Exceptions

#### Dead

Must be raised when the server declared the player's death. The process should end right after a `Dead` exception. The `Dead` exception must contain the name/role of the dead player.

Exemple of use:

```py
try:
    if data.sock.recv(1024).decode() == "dead":
        raise Dead(data.role)
except Dead as death:
    print(f"\033[0;31m{death.args[0]} Dead\033[0m")
    exit(0)
```

#### Forked

Must be raised when a process fork to handle the initialization of the newly created child process. It must contain the name of a strategy.

Example of use:

```py
try:
    id = os.fork()
    if id == 0:
        data.reset()
        raise Forked(strategy)
except Forked as frk:
    strategies[frk.args[0]](data)
```

#### ConnectionRefused

Must be raised if the client failed to connect to the server because the socket cannot be opened.

Example of use:

```py
try:
    data.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data.sock.connect((data.hostname, data.port))
except:
    raise ConnectionRefused(f"Failed to connect to {data.hostname}:{data.port}")
```

#### BroadcastReceived

Must be raised to handle received broadcast that must be prioritize over the initial player's strategy. The `BroadcastReceived` must contain the direction and the content of the message received without its headers. For example if the message received is "message 1 cat" the `BroadcastReceived` exception should contain "1 cat". If the message body itself have headers, they should be removed in the exception. For exemple if the message received is "message 1 team_cat" (where team is the team's name to verify if the broadcast is ally or not) the `BroadcastReceived` exception should contain "1 cat".

Example of use:

```py
try:
    received = data.sock.recv(1024).decode().split(" ")
    if received[0] == "message":
        raise BroadcastReceived(f"{received[1]} {received[2]}")
except BroadcastReceived as br:
    print("message received", br.args[0].split(" ")[1])
```

#### BroadcastDeny

Must be raised to handle a received broacast that isn't ally.

Exemple of use:

```py
try:
    received = data.sock.recv(1024).decode().split(" ")[2].split("_")
    if received[0] != data.team:
        raise BroadcastDeny
except BroadcastDeny:
    pass
```

### 0.2. Broadcast protocol

Each message broadcasted by our team must follow those rules:
- The broadcast MUST begin with 关塔那摩 which is the team's name in chinese.
- After the team's name, there MUST be the player's ID.
- The player's ID is a random number between 0 and 999999999 that SHOULD be traduced in chinese.
- After the player's ID, there MUST be the broadcast's number that SHOULD be traduced in chinese.
- The broadcast's number is the number of broadcasts the player has sent before this one.
- After the broadcast's number, there MUST be a message that SHOULD be traduced in chinese.
- Each of the above parts of the broadcast must be separated by a single `_`.
- There MUST not have `_`, ` ` of `\n` in the broadcast other than the places indicates by the last rule.
- After a message is sent, the broadcast's number should be incremented by 1.

There is examples of the broadcast of the second broadcast of player 761918518 that says "Hello everyone".

Examples of a well formated broadcasts of the same message:

```
关塔那摩_七亿六千万一百万九十万一万八千五百一十八_一_你们好
关塔那摩_761918518_1_HelloEveryone
关塔那摩_七六一九一八五一八_一_你们好
关塔那摩_761918518_一_你们好
关塔那摩_七亿六千万一百万九十万一万八千五百一十八_1_你们好
```

*The first one is the best according to the rules.*

Examples of bad formated broadcasts for the same message:

```
你们好
关塔那摩_你们好
关塔那摩_七亿六千万一百万九十万一万八千五百一十八_你们好
关塔那摩_一_你们好
七亿六千万一百万九十万一万八千五百一十八_一_你们好
关塔那摩 七亿六千万一百万九十万一万八千五百一十八 一 你们好
关塔那摩_七亿六千万一百万九十万一万八千五百一十八_一_你_们_好
关塔那摩_关塔那摩_一_你们好
```

*Those aren't exhaustives.*

## 1. Commands

### <ins>initialize</ins>

#### DESCRIPTION

Initialize a player.  
It reset the data structure, open the socket with the server then communicate with it to create the player.  
First it listen for the welcome send by the server. Then it send the team's name to the server. And finally it listen and store the number of free slot for the team and the map's dimensions.

#### USAGE

```py
from ai.commands import initialize

initialize(data)
```

With `data` an instance of the `Data` class that gather all the infos needed to work.

#### RETURN

Always `True`.

#### ERROR

If the connexion failed `ConnectionRefused` is raised.

### <ins>forward</ins>

#### DESCRIPTION

Ask the server to move the player one tile forward and listen for the server's answer.  
If the command succeed, data is updated according to the result of the command.

#### USAGE

```py
from ai.commands import forward

forward(data)
```

With `data` an instance of the `Data` class that gather all the infos needed to work.

#### RETURN

- `True` if the server answer with **ok**.
- `False` if the server answer with **ko**.

#### ERROR

If the player is dead, a `Dead` error is raised.

### <ins>right / left</ins>

#### DESCRIPTION

Ask the server to turn the player to its right / left and listen for the server's answer.  
If the command succeed, data is updated according to the result of the command.

#### USAGE

```py
from ai.commands import right, left

right(data)
left(data)
```

With `data` an instance of the `Data` class that gather all the infos needed to work.

#### RETURN

- `True` if the server answer with **ok**.
- `False` if the server answer with **ko**.

#### ERROR

If the player is dead, a `Dead` error is raised.

### <ins>look</ins>

#### DESCRIPTION

Ask the server to show what there are in front of the player. The eyesight of the player depend of its level.  
The result of the last look is stored in `data.map` as a list of `Tile` class instances.  
All the coordinates are relative to the player's position when the `data.map` were stored.

#### USAGE

```py
from ai.commands import look

look(data)
```

With `data` an instance of the `Data` class that gather all the infos needed to work.

#### RETURN

Always `True`.

#### ERROR

If the player is dead, a `Dead` error is raised.

### <ins>inventory</ins>

#### DESCRIPTION

Ask the server to show what's inside the player's inventory.  
It update the player's inventory in `data.player`.

#### USAGE

```py
from ai.commands import inventory

inventory(data)
```

With `data` an instance of the `Data` class that gather all the infos needed to work.

#### RETURN

Always `True`.

#### ERROR

If the player is dead, a `Dead` error is raised.

### <ins>broadcast</ins>

#### DESCRIPTION

Ask the server to diffuse a message to others players and listen for the server's answer.

#### USAGE

```py
from ai.commands import broadcast

broadcast(data, text)
```

With `data` an instance of the `Data` class that gather all the infos needed to work.  
And `text` is a `string` that contain informations to share with others players.

#### RETURN

Always `True`.

#### ERROR

If the player is dead, a `Dead` error is raised.

### <ins>connect_nbr</ins>

#### DESCRIPTION

Ask the server how many free slot are left for reproduction in our team.  
The answered number is updated in `data.remaining`.

#### USAGE

```py
from ai.commands import connect_nbr

connect_nbr(data)
```

With `data` an instance of the `Data` class that gather all the infos needed to work.

#### RETURN

Always `True`.

#### ERROR

If the player is dead, a `Dead` error is raised.

### <ins>reproduct</ins>

#### DESCRIPTION

Perform a process fork to create a new player.

#### USAGE

```py
from ai.commands import reproduct

reproduct(data)
```

With `data` an instance of the `Data` class that gather all the infos needed to work.

### <ins>fork</ins>

#### DESCRIPTION

Ask the server to create a new free slot for our team and listen for the server's answer.

#### USAGE

```py
from ai.commands import fork

fork(data)
```

With `data` an instance of the `Data` class that gather all the infos needed to work.

#### RETURN

- `True` if the server answer with **ok**.
- `False` if the server answer with **ko**.

#### ERROR

If the player is dead, a `Dead` error is raised.

### <ins>eject</ins>

#### DESCRIPTION

Ask the server to eject all others players from the current tile to the facing tile and listen for the server's answer.

#### USAGE

```py
from ai.commands import eject

eject(data)
```

With `data` an instance of the `Data` class that gather all the infos needed to work.

#### RETURN

- `True` if the server answer with **ok**.
- `False` if the server answer with **ko**.

#### ERROR

If the player is dead, a `Dead` error is raised.

### <ins>take</ins>

#### DESCRIPTION

Ask the server to make the player pick up one unit of the given ressource from the player's current tile and listen for the server's answer.  
If the command succeed, data is updated according to the result of the command.

#### USAGE

```py
from ai.commands import take

take(data, ressource)
```

With `data` an instance of the `Data` class that gather all the infos needed to work.  
And `ressource` is a `string` naming one of the ressources of the game.

#### RETURN

- `True` if the server answer with **ok**.
- `False` if the server answer with **ko**.

#### ERROR

If the player is dead, a `Dead` error is raised.

### <ins>set_down</ins>

#### DESCRIPTION

Ask the server to make the player drop one unit of the given ressource and listen for the server's answer.  
If the command succeed, data is updated according to the result of the command.

#### USAGE

```py
from ai.commands import set_down

set_down(data, ressource)
```

With `data` an instance of the `Data` class that gather all the infos needed to work.  
And `ressource` is a `string` naming one of the ressources of the game.

#### RETURN

- `True` if the server answer with **ok**.
- `False` if the server answer with **ko**.

#### ERROR

If the player is dead, a `Dead` error is raised.

### <ins>incantation</ins>

#### DESCRIPTION

Ask the server to cast a level up on the player and listen for the server's answer.  
If the command succeed, data is updated according to the result of the command.

#### USAGE

```py
from ai.commands import incantation

incantation(data)
```

With `data` an instance of the `Data` class that gather all the infos needed to work.

#### RETURN

- `True` if the server answer with **elevation underway**.
- `False` if the server answer with **ko**.

#### ERROR

If the player is dead, a `Dead` error is raised.

### <ins>pathfinding</ins>

#### DESCRIPTION

Use the `forward`, `right` and `left` commands to move the player to the given position.  
Remember that coordinates are relatives to the player's position when the last `look` has been cast.

#### USAGE

```py
from ai.algorithms import pathfinding

pathfinding(data, x, y)
```

With `data` an instance of the `Data` class that gather all the infos needed to work.  
The `x` and `y` are `integer` that represent the targeted coordinate.

#### RETURN

- `True` if the player succeed to reach the given position.
- `False` otherwise.

#### ERROR

If the player is dead, a `Dead` error is raised.

### <ins>gather</ins>

#### DESCRIPTION

Search for the case with the most of the given ressource then move the player to this position and finally take all of the ressource on the tile.

#### USAGE

```py
from ai.algorithms import gather

gather(data, ressource)
```

With `data` an instance of the `Data` class that gather all the infos needed to work.  
And `ressource` is a `string` naming one of the ressources of the game.

#### RETURN

- `True` if the player succeed to take at least one unit of the given ressource.
- `False` otherwise.

#### ERROR

If the player is dead, a `Dead` error is raised.

### <ins>attack</ins>

#### DESCRIPTION

Search for the case with the most players then move the player to this position and finally ejects the others players.

#### USAGE

```py
from ai.algorithms import attack

attack(data)
```

With `data` an instance of the `Data` class that gather all the infos needed to work.

#### RETURN

- `True` if the player succeed to eject at least one player.
- `False` otherwise.

#### ERROR

If the player is dead, a `Dead` error is raised.

### <ins>actualize</ins>

#### DESCRIPTION

Call `inventory` and `connect_nbr` to update the informations stored in `data`.

#### USAGE

```py
from ai.algorithms import actualize

actualize(data)
```

With `data` an instance of the `Data` class that gather all the infos needed to work.

#### RETURN

Always `True`.

#### ERROR

If the player is dead, a `Dead` error is raised.

## 2. Strategies

### <ins>worker</ins>

### <ins>recruiter</ins>

### <ins>parrot</ins>
