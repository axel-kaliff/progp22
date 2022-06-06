class GameCharacter:

    def __init__(self, position):

        self.position = position
        self.has_key = False
        self.on_pressure_plate = False

    # TODO change these to the actual commands?
    def calculate_move(self, direction):

        new_position = self.position[:]

        if direction == "LEFT":

            new_position[0] -= 1

        elif direction == "RIGHT":

            new_position[0] += 1

        elif direction == "UP":

            new_position[1] += 1

        elif direction == "DOWN":

            new_position[1] -= 1

        return new_position


class Game:

    # The initial (and unchanging) layout of the map

    start_position_1 = [4, 10]
    start_position_2 = [7, 10]

    left_wall = [[0,0], [0,1], [0,3], [0,4], [0,5], [0,6], [0,7], [0,8], [0,9], [0,10], [0,11], [0,12], [0,13], [0,14]]
    right_wall = [[19,0], [19,1], [19,3], [19,4], [19,5], [19,6], [19,7], [19,8], [19,9], [19,10], [19,11], [19,12], [19,13], [19,14]]
    lower_wall = [[1,0], [2,0], [3,0], [4,0], [5,0], [6,0], [7,0], [8,0], [9,0], [10,0], [11,0], [12,0], [13,0], [14,0], [15,0], [16,0], [17,0], [18,0], [19,0]]
    top_wall = [[1,14], [2,14], [3,14], [4,14], [5,14], [6,14], [7,14], [8,14], [9,14], [13,14], [14,14], [15,14], [16,14], [17,14], [18,14], [19,14]]
    final_room = [[5,15], [5,16], [5,17], [5,18], [5,19], [6,19], [7,19], [8,19], [9,19], [10,19], [11,19], [12,19], [13,19], [14,19], [14,18], [14,17], [14,16], [14,15]]
    key_room = [[13,1], [13,4], [13,5], [14,5], [15,5], [16,5], [17,5], [18,5]]
    
    big_door = [[10, 14], [11, 14], [12, 14]]
    small_door = [[13, 3], [13, 4]]

    key_position = [16, 3]
    prize_position = [10, 17]
    pressure_plate = [16, 8]

    def __init__(self):

        self.big_door_open = False
        self.small_door_open = False
        
        self.key_on_board = True

        self.game_won = False

        self.player1 = None
        self.player2 = None

        self.walls = self.left_wall + self.right_wall + self.lower_wall + self.top_wall + self.final_room + self.key_room

    # A new player is added to the board (up to two plqyers)
    # Returns:  The number of the player or None if the game already has two players
    def add_player(self):

        if self.player1 is None:

            self.player1 = GameCharacter(self.start_position_1)

            return 1

        elif self.player2 is None:

            self.player2 = GameCharacter(self.start_position_2)

            return 2

        return None

    # A player tries to move one square in a direction
    # Parameters:   player      the player should move
    #               direction   the direction in which the player moves
    # Returns:      True is the player moved, 
    #               False if the move was illegal and the player didn't move
    def move(self, player_number, direction):

        player = None

        if player_number == 1:
            player = self.player1
        elif player_number == 2:
            player = self.player2


        # The new position is calculated, but not moved to before conditions are checked
        new_position = player.calculate_move(direction)

        # A player can't move through walls
        if new_position in self.walls:

            print("WALL") #DEBUG
            return False

        # A player can't move  through the other player
        elif new_position == self.player1.position or new_position == self.player2.position:

            print("OTHER PLAYER") #DEBUG

            return False

        # A player can't move through a door if it's not open
        elif not self.small_door_open and new_position in self.small_door:

            print("SMALL DOOR") #DEBUG

            return False

        elif new_position in self.big_door and not player.has_key and not self.big_door_open:

            print("BIG DOOR") #DEBUG

            return False

        # Player moves to key position and picks up key
        elif self.key_on_board and new_position == self.key_position:

            player.position = new_position
            player.has_key = True

            return True

        # Player opens the big door with the key
        elif player.has_key and new_position in self.big_door:

            self.big_door_open = True
            player.position = new_position

            return True

        # The game is won and ends
        elif new_position == self.prize_position:

            self.game_won = True
            # TODO maybe make sure to end game when won?

            return True

        elif new_position == self.pressure_plate:

            self.small_door_open = True
            player.on_pressure_plate = True

            player.position = new_position

            return True

        # Player moves off pressure plate and small door closes
        elif player.on_pressure_plate:

            player.on_pressure_plate = False
            self.small_door_open = False

            player.position = new_position

            return True

        # All other moves are legal and uneventful
        else:

            player.position = new_position

            return True


if __name__ == "__main__":

    # Trial run of the game

    game = Game()
    print("Game started")
    first = game.add_player()
    second = game.add_player()

    print(f"Added players {first}:{game.player1.position}  and {second}:{game.player2.position}")

    print("Player 2")

    game.move(second, "RIGHT")
    print(game.player2.position)

    game.move(second, "RIGHT")
    print(game.player2.position)

    game.move(second, "RIGHT")
    print(game.player2.position)

    game.move(second, "RIGHT")
    print(game.player2.position)

    game.move(second, "RIGHT")
    print(game.player2.position)

    game.move(second, "RIGHT")
    print(game.player2.position)

    game.move(second, "RIGHT")
    print(game.player2.position)

    game.move(second, "RIGHT")
    print(game.player2.position)

    game.move(second, "RIGHT")
    print(game.player2.position)

    game.move(second, "DOWN")
    print(game.player2.position)

    game.move(second, "DOWN")
    print(game.player2.position)

    print("Player 1")

    game.move(first, "RIGHT")
    print(game.player1.position)

    game.move(first, "RIGHT")
    print(game.player1.position)

    game.move(first, "RIGHT")
    print(game.player1.position)

    game.move(first, "RIGHT")
    print(game.player1.position)

    game.move(first, "RIGHT")
    print(game.player1.position)

    game.move(first, "RIGHT")
    print(game.player1.position)

    game.move(first, "RIGHT")
    print(game.player1.position)

    game.move(first, "DOWN")
    print(game.player1.position)

    game.move(first, "DOWN")
    print(game.player1.position)

    game.move(first, "DOWN")
    print(game.player1.position)

    game.move(first, "DOWN")
    print(game.player1.position)

    game.move(first, "DOWN")
    print(game.player1.position)

    game.move(first, "DOWN")
    print(game.player1.position)

    game.move(first, "DOWN")
    print(game.player1.position)

    game.move(first, "RIGHT")
    print(game.player1.position)

    game.move(first, "RIGHT")
    print(game.player1.position)

    game.move(first, "RIGHT")
    print(game.player1.position)

    game.move(first, "RIGHT")
    print(game.player1.position)

    game.move(first, "RIGHT")
    print(game.player1.position)

    game.move(first, "RIGHT")
    print(game.player1.position)

    game.move(first, "RIGHT")
    print(game.player1.position)

    game.move(first, "RIGHT")
    print(game.player1.position)

    game.move(first, "RIGHT")
    print(game.player1.position)

    print(game.player1.has_key)

    game.move(first, "LEFT")
    print(game.player1.position)

    game.move(first, "LEFT")
    print(game.player1.position)

    game.move(first, "LEFT")
    print(game.player1.position)

    game.move(first, "LEFT")
    print(game.player1.position)

    game.move(first, "LEFT")
    print(game.player1.position)

    game.move(first, "LEFT")
    print(game.player1.position)

    game.move(first, "LEFT")
    print(game.player1.position)

    game.move(first, "UP")
    print(game.player1.position)

    game.move(first, "UP")
    print(game.player1.position)

    game.move(first, "UP")
    print(game.player1.position)

    game.move(first, "UP")
    print(game.player1.position)

    game.move(first, "UP")
    print(game.player1.position)

    game.move(first, "UP")
    print(game.player1.position)

    game.move(first, "UP")
    print(game.player1.position)

    game.move(first, "UP")
    print(game.player1.position)

    game.move(first, "UP")
    print(game.player1.position)

    game.move(first, "UP")
    print(game.player1.position)

    game.move(first, "UP")
    print(game.player1.position)

    game.move(first, "UP")
    print(game.player1.position)

    game.move(first, "UP")
    print(game.player1.position)

    game.move(first, "LEFT")
    print(game.player1.position)

    game.move(first, "UP")
    print(game.player1.position)

    print(game.game_won)

    game.move(first, "UP")
    print(game.player1.position)

    game.move(first, "UP")
    print(game.player1.position)

