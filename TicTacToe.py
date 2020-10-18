"""
Tim Withers
CS_372_400_S2020
Project 4
"""
import random

class TicTacToe:
	def __init__(self):
		self.gameboard = list()
		self.range = 9
		self.spacesFilled = 0
		self.rows = 3
		self.cols = 3
		self.playerTurn = 0			# Player 0 is 'x' and Player 1 is 'o'
		self.playerMarks = ['x', 'o']
		self.valid = False
		self.userInRow = -1
		self.userInCol = -1
		self.gameWon = False
		self.staleMate = False
		self.initBoard()
		self.chooseWhoStarts()
		self.gameplayloop()

	def chooseWhoStarts(self):
		# Random player to go first
		self.playerTurn = random.choice([0, 1])

	"""
	Init or reset board
	"""
	def initBoard(self):
		for i in range(9):
			self.gameboard.append('-')

	"""
	Reset board
	"""
	def reset(self):
		self.gameWon = False
		self.staleMate = False
		for i in range(9):
			self.gameboard.append('-')
		self.spacesFilled = 0

	"""
	Start the game
	"""
	def gameplayloop(self):
		self.drawBoard()

	"""
	This could be automated, but figured this was easy enough to hardcode. I don't ever
	plan on playing a NON 3x3 TicTacToe game.
	"""
	def drawBoard(self):
		print("**Tic Tac Toe**")
		print(("  c o l s\n  _| 0 | 1 | 2 |\nr 0| {} | {} | {} |\no 1| {} | {} | {} |\nw 2| {} | {} | {} |\n").format(self.gameboard[0],\
			self.gameboard[1], self.gameboard[2], self.gameboard[3], self.gameboard[4], self.gameboard[5], self.gameboard[6],\
			self.gameboard[7], self.gameboard[8]))

	def promptForMove(self):
		# Reset userInRow and col
		self.userInRow = -1
		self.userInCol = -1

		# Prompt user
		print("Please enter row and column for Player {}, '{}':".format(self.playerTurn+1, self.playerMarks[self.playerTurn]))

		# Get row from user
		while not self.valid:
			self.userInRow = input("Row: ")
			self.isValidRowRange(self.userInRow)

		# Reset valid flag
		self.valid = False

		# Get col from user
		while not self.valid:
			self.userInCol = input("Col: ")
			self.isValidColRange(self.userInCol)

		# Reset valid flag
		self.valid = False

		# Now that we've validated row/col input, check and make sure that spot is not already taken
		if self.isValidMove():
			# Put 'x' or 'o' onto board
			self.placeMarker()

			# Draw board
			self.drawBoard()
		else:
			self.promptForMove()

	"""
	Place a marker. For client/server interaction we don't need to manually
	switch over the playerTurn. Each player (client and server) will know
	which player they are.
	"""
	def placeMarker(self):
		if self.playerTurn == 0:
			self.gameboard[self.arrIndex()] = self.playerMarks[self.playerTurn]
			self.spacesFilled += 1

		elif self.playerTurn == 1:
			self.gameboard[self.arrIndex()] = self.playerMarks[self.playerTurn]
			self.spacesFilled += 1

	def isValidRowRange(self, x):
		try:
			self.userInRow = int(x)
			if self.userInRow in range(0, int(self.rows)):
				self.valid = True
				return True

			print("ERROR: Row input out of range. Try again.")
			return False

		except ValueError:
			print("ERROR: Row input not valid number. Try again.")
			return False
	
	def isValidColRange(self, x):
		try:
			self.userInCol = int(x)
			if self.userInCol in range(0, int(self.cols)):
				self.valid = True
				return True

			print("ERROR: Col input out of range. Try again.")
			return False

		except ValueError:
			print("ERROR: Col input not valid number. Try again.")
			return False

	"""
	Is the space we're trying to put a 'x' or 'o' already occupied? If so, return False.
	"""
	def isValidMove(self):
		if self.gameboard[self.arrIndex()] is not '-':
			print("ERROR: Spot already taken. Choose another.")
			return False

		return True

	def checkForWin(self):
		char = 'a'
		# Check vertical rows
		i = 0

		while i < self.rows:
			j = 0
			count = 0
			while j < self.range:
				# Get the character we're testing (either 'x' or 'o')
				if count == 0:
					char = self.gameboard[j+i]
				if char != '-' and self.gameboard[j+i] == char:
					count += 1
				j += 3

				if count == 3:
					if char == 'x':
						self.winningPlayer = 1
					elif char == 'o':
						self.winningPlayer = 2
					print("Vertical win by Player {}".format(self.winningPlayer))

					self.gameWon = True
					return True

			i += 1

		# Check horizontal rows
		i = 0
		
		while i < self.range:
			j = 0
			count = 0
			while j < self.cols:
				# Get the character we're testing (either 'x' or 'o')
				if count == 0:
					char = self.gameboard[j+i]
				if char != '-' and self.gameboard[j+i] == char:
					count += 1
				j += 1

				if count == 3:
					if char == 'x':
						self.winningPlayer = 1
					elif char == 'o':
						self.winningPlayer = 2
					print("Horizontal win by Player {}".format(self.winningPlayer))

					self.gameWon = True
					return True

			i += 3

		# Check diagonal rows
		count = 0
		char = self.gameboard[4]	# Center character
		if char != '-' and char == self.gameboard[0] and char == self.gameboard[8]:
			if char == 'x':
				self.winningPlayer = 1
			elif char == 'o':
				self.winningPlayer = 2
			print("Diagonal win by Player {}".format(self.winningPlayer))

			self.gameWon = True
			return True

		elif char != '-' and char == self.gameboard[2] and char == self.gameboard[6]:
			if char == 'x':
				self.winningPlayer = 1
			elif char == 'o':
				self.winningPlayer = 2
			print("Diagonal win by Player {}".format(self.winningPlayer))

			self.gameWon = True
			return True

		# Finally check for stalemate
		if self.spacesFilled >= self.range and not self.gameWon:
			self.staleMate = True
			print("STALE MATE. NO ONE WINS!")
			self.gameWon = True
			return True

		return False

	"""
	Add a marker to the board. This was added once working on the client/server interaction.
	"""
	def manualMarker(self, player, r=None, c=None):
		if self.playerTurn == 0:
			self.gameboard[self.arrIndex(r,c)] = self.playerMarks[player]
		elif self.playerTurn == 1:
			self.gameboard[self.arrIndex(r,c)] = self.playerMarks[player]

		self.spacesFilled += 1
		#self.checkForWin()


	"""
	Return 1d array index from 2d coords: (userIn, userCol)
	"""
	def arrIndex(self, r=None, c=None):
		if (r == 0 or r) and (c == 0 or c):
			return self.rows * r + c
		return (self.rows * self.userInRow + self.userInCol)

# game = TicTacToe()
# game.drawBoard()

# # Game loop
# while not game.checkForWin():
# 	game.promptForMove()