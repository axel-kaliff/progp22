# The Game

## Environment
2D board with different square types
Players occupy one square each

### square types
- Items
- Walls
- Empty

## start condition
two clients connected at the same time, that have checked that they're ready to play

## Win condition
The two players meet on the same square with one having more points than the other

## Movement
The player use arrow keys (or keys of choice) to move left,right, up, or down.

# Communication Protocol 

All game logic happens server-side.

Server sends info about player positions and board status to the player in a utf-8 string with the following structure: " [[square type]] [[Player name, player points, player x position, player y position]] "




