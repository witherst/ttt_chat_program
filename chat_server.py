"""
Tim Withers
CS_372_400_S2020
Project 4

I used the following resources to help write this file:

	https://www.youtube.com/watch?v=Lbfe3-v7yE0
		-- General setup and just watched the video to review client/server interaction
	https://www.youtube.com/watch?v=8A4dqoGL62E
		-- Using these techniques for a fixed length header in messages being sent

"""
import socket
from TicTacToe import *

"""
Header is of length 10 and is formatted as followed. 'Bits' 0 - 7:
0-6: Length of the message being sent
7: Row selection
8: Column selection
9: Whether a game is being played, '0' for no, '1' for yes
"""
HEADER_LENGTH = 10
H_LEN_BITS = 7	# As described above

PORT = 1105

"""
Send data with specified message
"""
def sendData(s):
	msg = input("YOU: ")
	msg = f'{len(msg):<{HEADER_LENGTH}}' + msg

	# If there is an instance of Tic Tac Toe, we're playing the game and have made a move
	if ttt:
		# This player would have made their move, so package up data into header
		msg = setGameBit(msg, 1)
		msg = setRowBit(msg, ttt.userInRow)
		msg = setColBit(msg, ttt.userInCol)

	s.send(bytes(msg, "utf-8"))

""" 
Receive data back from server. We'll use HEADER_LENGTH to get
the length of the message from the header.
"""
def receiveData(s):
	global ttt

	total_data = []
	data = ''

	full_msg = ''
	new_msg = True

	while True:
		msg = s.recv(16)

		# If this is the start of a new message, put HEADER_LENGTH in the header
		if new_msg:
			msglen = int(msg[:H_LEN_BITS].decode("utf-8"))
			new_msg = False

		# Decode to get full message
		full_msg += msg.decode("utf-8")

		if len(full_msg)-HEADER_LENGTH == msglen:
			truncated_msg = full_msg[HEADER_LENGTH:]
			header = full_msg[:HEADER_LENGTH]

			if truncated_msg == '/q':
				s.close()

			# Check to see if socket has been closed. If fileno() is -1, socket is closed.
			if s.fileno() == -1:
				break

			# Print what THEY said
			print(">>>THEM: {}".format(truncated_msg))
			new_msg = True
			full_msg = ''

			# Check to see if a gamebit is set
			if getGameBit(header) == 1:
				initgame()
				# Update game with other player's move
				updategame(header)

				if not ttt.gameWon:
					ttt.drawBoard()
					# Check for win now
					ttt.checkForWin()

					# Prompt only if game not won
					if not ttt.gameWon:
						ttt.promptForMove()
						# Check for win after WE placed a move
						ttt.checkForWin()

			# Now send something back
			sendData(s)

"""
Create instance of TicTacToe
"""
def initgame():
	global ttt

	if not ttt:
		ttt = TicTacToe()
		ttt.playerTurn = 1	# Setting this manually.
	else:
		ttt.reset()

"""
Check to see if the other player went, if they did, update OUR game board with their move.
"""
def updategame(h):
	global ttt

	# If the other player has made a move, update our game board
	r = getRowBit(h)
	c = getColBit(h)

	if (r == 0 or r) and (c == 0 or c):
		ttt.manualMarker(0, r, c)	# Place a manual marker for Player 0

"""
Creating a couple of helper functions for easier header manipulation
"""
def setGameBit(msg, val):
	temp = msg[:9] + str(val) + msg[10:]
	return temp

def setColBit(msg, c):
	temp = msg
	if c != -1:
		temp = msg[:8] + str(c) + msg[9:]
	return temp

def setRowBit(msg, r):
	temp = msg
	if r != -1:
		temp = msg[:7] + str(r) + msg[8:]
	return temp

def getGameBit(header):
	try:
		return int(header[9])
	except ValueError:
		pass

def getColBit(header):
	try:
		return int(header[8])
	except ValueError:
		pass

def getRowBit(header):
	try:
		return int(header[7])
	except ValueError:
		pass

"""
Main program
"""
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	# SOCK_STEAM = TCP protocol
s.bind((socket.gethostname(), PORT))

print("Server online. Listening for connections.")

# Set server to listen for 1 connection
s.listen(1)
ttt = None

# Forever listen for connections
while True:
	# address is the IP of the connecting client
	clientsocket, address = s.accept()

	print(f"\nConnection from {address} has been established")
	print(f"Waiting for for message from client...")

	# Receive data
	receiveData(clientsocket)

	if clientsocket.fileno() == -1:
		print("Connection closed. Ending session.")
		break

	# Close socket
	#clientsocket.close()