# The Game

## Environment
2D board with different square types
Players occupy one square each

### square types
- Items (levels player up when players steps on the same square)
- Walls
- Empty

## Starting 
Two clients connected at the same time, that have checked that they're ready to play. 

Players start at diagonally opposite positions, one at (0,0) one at (n,n), n being the set side length of the board.

## Winning 
The two players meet on the same square with one having more points than the other

## Movement
The player use arrow keys (or keys of choice) to move left,right, up, or down.

# Communication Protocol 

All game logic happens server-side.

## Handshake

When a client connects server sends info about player ID, initial positions and board side length

## Server -> Client


### Before the game
Before two players have joined the session, the server will output a "0" to signal that it is waiting for one more player before the game can begin.

### During the game

The different sections of game data is seperated by "|" and in cases where there are multiple data entries within two "|"s, the data entries are seperated by a blank space " ".

Coordinate data is always two integers (possible multiple digits) seperated by a ",".

The order of the data sectiona is as following (data with multiple entries marked with an "m" in parentheses):

- Wall coordinates (m)
- Door coordinates (m)
- Key coordinates
- Trophy coordinates
- Pressure plate coordinates
- Player coordinates (m)

### After the game
When one player reaches the trophy, the game is one and the server will output a "1" to all connected clients.


## Client -> Server
Client sends player command to server in UTF-8 string 

The command represents the direction the player wants to move, and is one of four directions:

- "RIGHT"
- "LEFT"
- "UP"
- "DOWN"

The commands must be in uppercase to be accepted by the server

