from enum import Enum
class Orientation(Enum):
    HORIZONTAL = 1
    VERTICAL = 2

class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.isFiredUpon = False
        self.ship = None
        
    def markFired(self):
        self.isFiredUpon = True

class Ship:
    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.positions = []  # List of Cell objects
        
    def isSunk(self):
        # Ship is sunk if all cells in positions have been fired upon
        return all(cell.isFiredUpon for cell in self.positions)

class Board:
    def __init__(self, size=10):
        self.size = size
        self.grid = [[Cell(row, col) for col in range(size)] for row in range(size)]
        self.ships = []
        
    def isValidPlacement(self, ship, start_row, start_col, orientation):
        # Check boundaries and overlapping ships
        if orientation == Orientation.HORIZONTAL:
            if start_col + ship.size > self.size:
                return False
            for col in range(start_col, start_col + ship.size):
                if self.grid[start_row][col].ship is not None:
                    return False
        else:  # Orientation.VERTICAL
            if start_row + ship.size > self.size:
                return False
            for row in range(start_row, start_row + ship.size):
                if self.grid[row][start_col].ship is not None:
                    return False
        return True
        
    def placeShip(self, ship, start_row, start_col, orientation):
        if not self.isValidPlacement(ship, start_row, start_col, orientation):
            raise ValueError("Invalid ship placement.")
        if orientation == Orientation.HORIZONTAL:
            for col in range(start_col, start_col + ship.size):
                cell = self.grid[start_row][col]
                cell.ship = ship
                ship.positions.append(cell)
        else:
            for row in range(start_row, start_row + ship.size):
                cell = self.grid[row][start_col]
                cell.ship = ship
                ship.positions.append(cell)
        self.ships.append(ship)
        
    def receiveAttack(self, row, col):
        cell = self.grid[row][col]
        if cell.isFiredUpon:
            return "Already Attacked"
        cell.markFired()
        if cell.ship:
            if cell.ship.isSunk():
                return f"Hit and sunk {cell.ship.name}!"
            return "Hit!"
        return "Miss!"
        
    def allShipsSunk(self):
        return all(ship.isSunk() for ship in self.ships)

class Player:
    def __init__(self, name):
        self.name = name
        self.board = Board()
        
    def makeMove(self, opponentBoard, row, col):
        return opponentBoard.receiveAttack(row, col)
    
    def hasLost(self):
        return self.board.allShipsSunk()

class Game:
    def __init__(self, player1Name, player2Name):
        self.player1 = Player(player1Name)
        self.player2 = Player(player2Name)
        self.currentPlayer = self.player1
        
    def switchTurns(self):
        self.currentPlayer = self.player2 if self.currentPlayer == self.player1 else self.player1
        
    def playTurn(self, row, col):
        opponent = self.player2 if self.currentPlayer == self.player1 else self.player1
        result = self.currentPlayer.makeMove(opponent.board, row, col)
        print(f"{self.currentPlayer.name} attacked ({row}, {col}): {result}")
        if opponent.hasLost():
            print(f"{self.currentPlayer.name} wins!")
            return True  # Game over
        self.switchTurns()
        return False  # Game continues

# Example of how the game might be started:
if __name__ == "__main__":
    game = Game("Alice", "Bob")
    # Place ships for players. For example:
    ship1 = Ship("Destroyer", 2)
    game.player1.board.placeShip(ship1, 0, 0, Orientation.HORIZONTAL)
    # ... Place remaining ships for both players.
    
    # Simulate some moves
    gameOver = False
    while not gameOver:
        # For demonstration, we pick random coordinates (in a real game, you would get input)
        row, col = 0, 0  # Replace with actual move logic
        gameOver = game.playTurn(row, col)


# Step 1: Clarify Requirements and Assumptions

# You could start by asking clarifying questions such as:
# 	•	Game Mode: Is it a two-player game (human vs. human) or do we also need to support playing against an AI?
# 	•	Interface: Is this a console game or does it have a graphical interface?
# 	•	Rules: Are we following the standard Battleship rules? (e.g., board size is 10x10, ships of various sizes, etc.)
# 	•	Functional Requirements:
# 	•	Players place ships on their boards.
# 	•	Players take turns guessing coordinates.
# 	•	The system should indicate a hit or a miss.
# 	•	A ship is sunk when all of its cells are hit.
# 	•	The game ends when one player’s fleet is completely sunk.
# 	•	Non-Functional Requirements: Responsiveness, extensibility (maybe later add network play), etc.

# For the purpose of the LLD, assume a two-player game played in a console.

# 	1.	Cell
# 	•	Responsibility: Represents a single coordinate on the board.
# 	•	Attributes:
# 	•	row: Integer.
# 	•	col: Integer.
# 	•	isFiredUpon: Boolean.
# 	•	ship: Reference to a Ship if one is placed here (or null if empty).
# 	•	Methods:
# 	•	markFired(): Marks the cell as fired upon.
# 	2.	Ship
# 	•	Responsibility: Represents a ship that occupies one or more cells on the board.
# 	•	Attributes:
# 	•	name: String (e.g., “Battleship”, “Cruiser”).
# 	•	size: Integer.
# 	•	orientation: Enum or String (e.g., “HORIZONTAL”, “VERTICAL”).
# 	•	positions: List of Cell objects that this ship occupies.
# 	•	Methods:
# 	•	isSunk(): Returns true if all cells in positions have been hit.
# 	•	placeShip(startCell, orientation): Sets the cells for the ship given a starting cell and orientation.
# 	3.	Board
# 	•	Responsibility: Represents the game board for a player.
# 	•	Attributes:
# 	•	grid: 2D array (or matrix) of Cell objects.
# 	•	ships: List of Ship objects placed on this board.
# 	•	size: Integer (e.g., 10 for a 10x10 board).
# 	•	Methods:
# 	•	placeShip(ship, startCell, orientation): Places a ship if the placement is valid.
# 	•	isValidPlacement(ship, startCell, orientation): Validates that the ship can be placed (i.e., within boundaries and not overlapping).
# 	•	receiveAttack(row, col): Marks the cell as fired upon and returns the result (hit, miss, or sunk).
# 	•	allShipsSunk(): Returns true if all ships on the board have been sunk.
# 	4.	Player
# 	•	Responsibility: Represents a player in the game.
# 	•	Attributes:
# 	•	name: String.
# 	•	board: The player’s own Board (with their ships).
# 	•	opponentBoardView: A board or data structure to track hits/misses on the opponent’s board (optional, for UI purposes).
# 	•	Methods:
# 	•	makeMove(opponentBoard, row, col): Calls opponentBoard’s receiveAttack method.
# 	•	hasLost(): Returns true if all ships on the player’s board are sunk.
# 	5.	Game
# 	•	Responsibility: Orchestrates the overall gameplay.
# 	•	Attributes:
# 	•	player1: Player.
# 	•	player2: Player.
# 	•	currentPlayer: Reference to the player whose turn it is.
# 	•	Methods:
# 	•	start(): Initializes the game, boards, and ships.
# 	•	switchTurns(): Switches currentPlayer.
# 	•	playTurn(row, col): Processes a move from the current player.
# 	•	checkWinner(): Determines if the game is over and who won.
# 	•	displayBoards(): (For a console game) prints out the boards for each player.

#     Step 3: Explain Interactions and Flow
# 	1.	Initialization:
# 	•	The Game object creates two Player objects.
# 	•	Each Player creates and initializes their Board (with a 10x10 grid).
# 	•	Players place their ships on the board using the placeShip method on the Board class. The board checks for valid placements.
# 	2.	Gameplay Loop:
# 	•	The Game enters a loop where the currentPlayer calls makeMove on the opponent’s board.
# 	•	The opponent’s board processes the move via receiveAttack:
# 	•	It marks the corresponding Cell as fired upon.
# 	•	If a Cell contains part of a Ship, that cell is recorded as a hit.
# 	•	The Ship’s isSunk() method may be called to check if it is fully destroyed.
# 	•	The game then calls checkWinner() to determine if the game should end.
# 	•	The Game switches turns via switchTurns() and the loop repeats.
# 	3.	Ending the Game:
# 	•	The game loop exits when one of the players has no remaining ships (i.e., allShipsSunk() returns true on their board).
# 	•	The game announces the winner.