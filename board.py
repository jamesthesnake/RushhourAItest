# File: Board.py

import copy
import time
class Board:
# Class: Board
# Description: This class has all of the state generation 
#	           methods for each state. Since 'Board' itself
#	           holds a state of the game, this lets us look 
#              at exactly what that state looks like.
	vehiclefindtime = 0
	vehiclemovetime = 0
	checkwintime = 0
	doactiontime = 0
	copytime = 0
	def __init__(self):
	# Function: __init__
	# Paramaters: The Instance of Board
	# Description: Initializes a new Board object for use
	# in the Rush Hour puzzle.  
		self.spaces = []
	
	def __eq__(self, b):
	# Function: __eq__
	# Parameters: The Instance of Board, and another Board
	# Description: Takes another board, and sees if its state is equal to the
	#              state of this board.
	# Returns: 1 if the spaces are equal, 0 if not
		if self.spaces == b.spaces:
			return 1
		else:
			return 0
			
	def loadBoard(self, filename):
	# Function: loadBoard
	# Description: Takes a string that is a filename, and loads a Rush Hour board
	#		         into memory.
	# Parameters: Instance of Board, Name of the file to be loaded (string)
	# Returns: 1 if successful, 0 if unsuccessful
		try:
			infile = open(filename)
		except IOError:
			return 0
		
		size = infile.readline()
		board = infile.readlines()
		for y in board:
			yspaces = []
			for x in y:
				if x != '\r' and x != '\n':
					yspaces.append(x)
			if yspaces != []:
				self.spaces.append(yspaces)
		return 1
	
	def printDisplay(self):
	# Function: printDisplay
	# Description: Takes what the current state looks like, and outputs it to 
	#              the screen.
	# Parameters: Instance of Board
	# Returns: Nothing
		out = ""
		for y in self.spaces:
			for x in y:
				out = out + x
			out = out + '\n'
		print out
	
	def getSize(self):
	# Function: getSize
	# Description: Returns the size of the Rush Hour board
	# Parameters: The Instance of Board
	# Returns: An integer, that is the size of the Rush Hour board (not
	#          including the exit space)
		return self.spaces.size()
	
	def whatCanMove(self):
	# Function: whatCanMove
	# Description: Takes what the current state looks like, and determines what
	#              actions are valid to be taken from this state, and returns 
	#              a list of them in the form of:
	#              [[Display character, [Coordinates occupied], Whether or not
	#                it's the escape car, the vehicle's orientation], and the
	#				 direction the car can go]
	# Parameters: Instance of Board
	# Returns: A list holding all actions that can validly take place to 
	#          create a new state
		alreadyfound = []
		vehicles = []
		movablevehicles = []
		coord = []
		vehiclecoord = []
		orientation = 'y'
		escape = 0
		alreadyfound.append('-')
		alreadyfound.append('.')
		
		#Build a list of vehicles
		vtime = time.time()
		for y in self.spaces:
			for x in y:
				escape = 0
				if x not in alreadyfound:
					alreadyfound.append(x)
					vehiclecoord.append([y.index(x), self.spaces.index(y)])
					if y.index(x) + 1 < len(y) and y[y.index(x) + 1] == x:
						vehiclecoord.append([y.index(x) + 1, self.spaces.index(y)])
						if y.index(x) + 2 < len(y) and y[y.index(x) + 2] == x:
							vehiclecoord.append([y.index(x) + 2, self.spaces.index(y)])
						orientation = 'x'
					if y.index(x) - 1 >= 0 and y[y.index(x) - 1] == x:
						vehiclecoord.append([y.index(x) - 1, self.spaces.index(y)])
						if y.index(x) - 2 >= 0 and y[y.index(x) - 2] == x:
							vehiclecoord.append([y.index(x) - 2, self.spaces.index(y)])
						orientation = 'x'
					if self.spaces.index(y) + 1 < len(self.spaces) and \
					   self.spaces[self.spaces.index(y) + 1][y.index(x)] == x:
						vehiclecoord.append([y.index(x), self.spaces.index(y) + 1])
						if self.spaces.index(y) + 2 < len(self.spaces) and \
						   self.spaces[self.spaces.index(y) + 2][y.index(x)] == x:
							vehiclecoord.append([y.index(x), self.spaces.index(y) + 2])
						orientation = 'y'
					if self.spaces.index(y) - 1 >= 0 and \
					   self.spaces[self.spaces.index(y) - 1][y.index(x)] == x:
						vehiclecoord.append([y.index(x), self.spaces.index(y) - 1])
						if self.spaces.index(y) - 2 >= 0 and \
						   self.spaces[self.spaces.index(y) - 2][y.index(x)] == x:
							vehiclecoord.append([y.index(x), self.spaces.index(y) - 2])
						orientation = 'y'
					if x == '?':
						escape = 1
					vehicles.append([x, vehiclecoord, escape, orientation])
					vehiclecoord = []
		vtime = time.time() - vtime
		Board.vehiclefindtime = Board.vehiclefindtime + vtime
		#Find what vehicles can validly move	
		mtime = time.time()
		for v in vehicles:
			for coord in v[1]:
        
				if v[3] == 'x' and (coord[0] - 1 >= 0) and \
				   self.spaces[coord[1]][coord[0] - 1] == '.':
					movablevehicles.append([v, -1])
				if v[3] == 'x' and (coord[0] + 1 < len(self.spaces[coord[1]])) and \
				   (self.spaces[coord[1]][coord[0] + 1] == '.' or \
				    self.spaces[coord[1]][coord[0] + 1] == '-'):
					movablevehicles.append([v, 1])
				if v[3] == 'y' and (coord[1] + 1 < len(self.spaces)) and \
				   self.spaces[coord[1] + 1][coord[0]] == '.':
					movablevehicles.append([v, 1])
				if v[3] == 'y' and (coord[1] - 1 >= 0) and \
				   self.spaces[coord[1] - 1][coord[0]] == '.':
					movablevehicles.append([v, -1])
		mtime = time.time() - mtime
		Board.vehiclemovetime = Board.vehiclemovetime + mtime
		return movablevehicles
	
	def isAWin(self):
	# Function: isAWin
	# Description: Determines whether or not the current state is a goal state
	# Parameters: The instance of Board
	# Returns: 1 if it's in a goal state, 0 if not
		cwin = time.time()
		for y in self.spaces:
			if '?' in y:
				if y.index('?') == len(self.spaces) - 1:
					cwin = time.time() - cwin
					Board.checkwintime += cwin
					return 1
		cwin = time.time() - cwin
		Board.checkwintime += cwin
		return 0

	def printAction(self, action):
	# Function: printAction
	# Description: Takes an action, and prints out a useful dialog about it.
	# Parameters: The instance of board, and an action in the form of:
	#              [[Display character, [Coordinates occupied], Whether or not
	#                it's the escape car, the vehicle's orientation], and the
	#				 direction the car can go]
	# Returns: Nothing
		if action == None:
			print "No action"
		else:
			if action[0][3] == 'x':
				if action[1] == -1:
					print action[0][0], "moving left."
				else:
					print action[0][0], "moving right."
			else:
				if action[1] == -1:
					print action[0][0], "moving up."
				else:
					print action[0][0], "moving down."

	def doAction(self, action):
	# Function: doAction
	# Description: Takes an action, and the current state, and creates a new
	#              state.
	# Parameters: The instance of board, and an action in the form of:
	#              [[Display character, [Coordinates occupied], Whether or not
	#                it's the escape car, the vehicle's orientation], and the
	#				 direction the car can go]
	# Returns: A Board instance, which is the new state.
		dtime = time.time()
		copytime = time.time()
		temp = []
		newboard = Board()
		for y in self.spaces:
			for x in y:
				temp.append(x)
			newboard.spaces.append(temp)
			temp = []
		copytime = time.time() - copytime
		Board.copytime += copytime
		if action[0][3] == 'x':
			leftbehind = 0
			y = 0
			if action[1] > 0:
				leftbehind = len(newboard.spaces)
				for t in action[0][1]:
					y = t[1]
					newboard.spaces[t[1]][t[0] + 1] = action[0][0]
					if t[0] < leftbehind:
						leftbehind = t[0]
			else:
				leftbehind = -1
				for t in action[0][1]:
					y = t[1]
					newboard.spaces[t[1]][t[0] - 1] = action[0][0]
					if t[0] > leftbehind:
						leftbehind = t[0]
			newboard.spaces[y][leftbehind] = '.'
		else:
			leftbehind = 0
			x = 0
			if action[1] > 0:
				leftbehind = len(newboard.spaces)
				for t in action[0][1]:
					x = t[0]
					newboard.spaces[t[1] + 1][t[0]] = action[0][0]
					if t[1] < leftbehind:
						leftbehind = t[1]
			else:
				leftbehind = -1
				for t in action[0][1]:
					x = t[0]
					newboard.spaces[t[1] - 1][t[0]] = action[0][0]
					if t[1] > leftbehind:
						leftbehind = t[1]
			newboard.spaces[leftbehind][x] = '.'
		dtime = time.time() - dtime
		Board.doactiontime += dtime
		return newboard
