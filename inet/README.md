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
Server sends info about player positions and board status to the player in a utf-8 string with the following structure: "[{1}],{2,3,4,5}] "

Where:
- 1 = Square type
- 2 = Player ID
- 3 = Player level
- 4 = Player X-position
- 5 = Player Y-position

The {} means repeating entries. Square entries are sent as one sequence, being broken up into rows by the client based on initial conditions sent by server

## Client -> Server
Client sends player comamand to server in utf-8 string: "command code"

Command codes:

- 1 = left
- 2 = right
- 3 = up
- 4 = down
