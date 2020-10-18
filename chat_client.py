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
import time
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
FIRST_MSG = True		# Will be used to send '/q' instructions to client on the first message

""" 
Receive data back from server. We'll use HEADER_LENGTH to get
the length of the message from the header.
"""
def receiveData(s):
	global ttt
	# Make socket not blocking
	#s.setblocking(0)

	total_data = []
	data = ''

	full_msg = ''
	new_msg = True

	while True:
		# Check to see if socket has been closed. If fileno() is -1, socket is closed.
		if s.fileno() == -1:
			print("Connection closed. Ending session.")
			break

		# Receive from server
		msg = s.recv(16)
		if new_msg:
			msglen = int(msg[:H_LEN_BITS].decode("utf-8"))
			new_msg = False

		full_msg += msg.decode("utf-8")

		# If we received the full message
		if len(full_msg)-HEADER_LENGTH == msglen:
			header = full_msg[:HEADER_LENGTH]
			print(">>>THEM: {}".format(full_msg[HEADER_LENGTH:]))
			new_msg = True
			full_msg = ''

			# Check to see if a gamebit is set
			if getGameBit(header) == 1:
				initgame()
				ttt.playerTurn = 0	# Setting this manually, client is always player 1 (or 0 in array index land)
				updategame(header)

				if not ttt.gameWon:
					ttt.drawBoard()
					# Check for win now
					ttt.checkForWin()

			break

	# Check to see if socket has been closed. If fileno() is -1, socket is closed.
	if s.fileno() != -1:
		sendData(s)

"""
Send data with specified message
"""
def sendData(s):
	global ttt

	msg = input("YOU: ")
	if msg:
		gameCheck = msg[:2]

	# Create message
	msg = f'{len(msg):<{HEADER_LENGTH}}' + msg

	# Check to see if a game wants to be played
	if ttt or (gameCheck[0] == '/' and gameCheck[1] == 'g'):
		initgame()
		msg = setGameBit(msg, 1)

	# If player turn is 0, we will go first, if not, the other player goes first
	if ttt and ttt.playerTurn == 0 and not ttt.gameWon:
		ttt.promptForMove()
		ttt.checkForWin()		

		# This player would have made their move, so package up and send to other player
		msg = setGameBit(msg, 1)
		msg = setRowBit(msg, ttt.userInRow)
		msg = setColBit(msg, ttt.userInCol)

	# Send message
	s.send(bytes(msg, "utf-8"))

	if msg and msg[HEADER_LENGTH:] == '/q':
		s.close()

	receiveData(s)

"""
Create instance of TicTacToe and start the run
"""
def initgame():
	global ttt

	if not ttt:
		ttt = TicTacToe()
	else:
		ttt.reset()

"""
Check to see if the other player went, if they did, update OUR game board.
"""
def updategame(h):
	global ttt

	# If the other player has made a move, update our game board
	r = getRowBit(h)
	c = getColBit(h)

	# Annoyingly have to check if r == 0. Because if r == 0, just saying "if r" will be false...we don't want that.
	if (r == 0 or r) and (c == 0 or c):
		ttt.manualMarker(1, r, c)

"""
Creating a couple of helper functions for easier header manipulation
"""
def setGameBit(msg, val):
	temp = msg[:9] + str(val) + msg[10:]
	return temp

def setColBit(msg, c):
	temp = msg
	if c != '-':
		temp = msg[:8] + str(c) + msg[9:]
	return temp

def setRowBit(msg, r):
	temp = msg
	if r != '-':
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

# Create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Set server and default HTTP port
hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)

# Connect to server
s.connect((hostname, PORT))

print(f"\nConnection to {ip}:{PORT} has been established.")
print("Type /q to quit and close connection.\nType /g to start a game of Tic Tac Toe.")

# Receive data
ttt = None
sendData(s)