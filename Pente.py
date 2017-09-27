from copy import *

class Pente:
	"""Class for a state in a game of Pente"""
	
	def __init__(self, winner=None, turn=1, playerToMove=0, captures=(0,0), positions=(0,0)):
		"""Initialize a game.  Defaults to a new game.
		
		   Each component of positions store where each of the players has moved on the 19x19 board.
		   These are stored in binary as a 361 bit integer in row major order."""
		self._winner = winner	# Other options are 0 and 1, 'Tie'
		self._turn = turn
		self._playerToMove = playerToMove
		self._captures = captures
		self._positions = positions
		
		
	def winner(self):
		"""Return the winner of the game, None if it is still going."""
		return self._winner
		
	def turn(self):
		"""The turn the game is currently on."""
		return self._turn
		
	def playerToMove(self):
		"""Return 0 or 1 based on whose players turn it is."""
		return self._playerToMove
		
	def captures(self):
		"""Return the number of captures that have occured."""
		return self._captures
		
	def legalMove(self, move):
		"""Test wheter a move, represented a pair (row,column) is a legal move."""
		if not 0 <= move[0] < 19:
			return False
		if not 0 <= move[0] < 19:
			return False
			
		if self._turn == 1:
			return move == (9,9)
		if self._turn == 3:
			if 7 <= move[0] <= 11 and 7 <= move[1] <= 11:
				return False
			
		mask = 1 << (19*move[0]+move[1])
		if mask & self._positions[0] != 0 or mask & self._positions[1] != 0:
			return False
			
		return True
		
	def position(self, pos):
		"""Return None, 0, or 1 based on what at the given position represented as a pair (row,column)."""
		if not (0 <= pos[0] < 19):
			return None
		if not (0 <= pos[1] < 19):
			return None
		
		mask = 1 << (19*pos[0]+pos[1])
		if mask & self._positions[0] != 0:
			return 0
		if mask & self._positions[1] != 0:
			return 1
		return None
		
	def isCapture(self, move, player):
		"""Is the move a capture for the given player."""
		for direction in [ (1,0), (-1,0), (0,1), (0,-1), (1,1), (1,-1), (-1,1), (-1,-1) ]:
			if self.position( (move[0]+direction[0], move[1]+direction[1]) ) == 1-player:
				if self.position( (move[0]+2*direction[0], move[1]+2*direction[1]) ) == 1-player:
					if self.position( (move[0]+3*direction[0], move[1]+3*direction[1]) ) == player:
						return True
		return False		
	
	def isFiveInARow(self, move, player):
		"""Does the move give five in a row for the player."""
		
		for direction in [ (1,0), (0,1), (1,1), (1,-1) ]:
			num = 0
			for r in range(1,6):
				if self.position( (move[0]+r*direction[0], move[1]+r*direction[1]) ) == player:
					num += 1
				else:
					break
			for r in range(1,6):
				if self.position( (move[0]-r*direction[0], move[1]-r*direction[1]) ) == player:
					num += 1
				else:
					break
			if num >= 4:
				return True
		return False
		
	def applyMove(self, move):
		"""Return a new Pente state after the move (assumed to be legal) is applied."""
		mask = 1 << (19*move[0]+move[1])
		
		newPos = list(self._positions)
		newPos[self._playerToMove] |= mask
			
		winner = None
		newCap = list(self._captures)
		if self.isCapture(move, self._playerToMove):
			newCap[self._playerToMove] += 1
			newCap = tuple(newCap)
			
			if newCap[self._playerToMove] == 5:
				winner = self._playerToMove
				
			# Apply the capture
			for direction in [ (1,0), (-1,0), (0,1), (0,-1), (1,1), (1,-1), (-1,1), (-1,-1) ]:
				if self.position( (move[0]+direction[0], move[1]+direction[1]) ) == 1-self._playerToMove:
					if self.position( (move[0]+2*direction[0], move[1]+2*direction[1]) ) == 1-self._playerToMove:
						if self.position( (move[0]+3*direction[0], move[1]+3*direction[1]) ) == self._playerToMove:
							mask1 = 1 << (19*(move[0]+direction[0]) + move[1]+direction[1])
							mask2 = 1 << (19*(move[0]+2*direction[0]) + move[1]+2*direction[1])
							newPos[1-self._playerToMove] &= (1<<361) - 1 - mask1 -mask2
				
		if self.isFiveInARow(move, self._playerToMove):
			winner = self._playerToMove
			
		if newPos[0] | newPos[1] + 1 == (1 << 361):
			winner = 'Tie'
			
		return Pente(winner, self._turn+1, 1-self._playerToMove, newCap, tuple(newPos))

	def patternCount(self, pattern):
		"""Count how many times a pattern occurs in a row, column or diagonal.
		
		   The pattern is specified with a string, spaces representing blank positions,
		   and 0 and 1's representing the two players."""
		   
		patternsToCheck = set()
		patternsToCheck.add(pattern)
		patternsToCheck.add(pattern[::-1])
		
		count = 0
		for p in patternsToCheck:
			for direction in [ (1,0), (0,1), (1,1), (1,-1) ]:
				if p[0] == ' ':
					current = (1 << 361) - 1 - (self._positions[0] | self._positions[1])
				elif p[0] == 'W':
					current = deepcopy(self._positions[0])
				else:
					current = deepcopy(self._positions[1])
				
				shiftAmount = 19*direction[0] + direction[1]
				for i in range(1,len(pattern)):
					current <<= shiftAmount;
					if direction[0] > 0:
						current &= (1<<361) - 1
					if direction[1] > 0:
						current &= 4697076206551609815682113896275491678163628321270401103722361051487966479967031806586121315490015370351738878L
					if direction[1] < 0:
						current &= 2348538103275804907841056948137745839081814160635200551861180525743983239983515903293060657745007685175869439L

					if p[i] == ' ':
						current &= (1 << 361) - 1 - self._positions[0] - self._positions[1]
					elif p[i] == 'W':
						current &= self._positions[0]
					else:
						current &= self._positions[1]

				count += bin(current).count("1")
			
		return count

	def display(self):
		"""Print out the current state."""
		
		print 'Turn', self._turn
		print 'Captures', ' white:', self._captures[0], 'black:', self._captures[1]
		if self._winner is None:
			print ['White','Black'][self._playerToMove], 'to move'
		elif self._winner == 'Tie':
			print 'Game is a tie'
		else:
			print ['White','Black'][self._winner], 'won'
			
		s1 = '   '
		s2 = '   '
		for c in range(19):
			if c < 10:
				s1 += '0'
			else:
				s1 += '1'
			s2 += str(c%10)
		print s1
		print s2
		print
		for r in range(19):
			s = "%02d " % r
			for c in range(19):
				p = self.position((r,c))
				if p is None:
					s += " "
				elif p == 0:
					s += "W"
				else:
					s += "B"
			print s + " %02d" % r
		
		print	
		s1 = '   '
		s2 = '   '
		for c in range(19):
			if c < 10:
				s1 += '0'
			else:
				s1 += '1'
			s2 += str(c%10)
		print s1
		print s2

	def evaluateMove(self, move):
		"""Determine the number of sequences of varies length that will be completed by filling in the position.
		
		   It returns two lists:
		     openEnded[player] which counts the number of sequences of each length that have empty positions at both ends for given player
		     halfOpenEdned[player] which counts the number of sequences of each length that have empty positions at one end for given player
		"""
		
		openEnded = []
		halfOpenEnded = []
		for i in range(2):
			openEnded.append( [0]*6 )
			halfOpenEnded.append( [0]*6 )
			
		for player in range(2):
			for direction in [ (1,0), (0,1), (1,1), (1,-1) ]:
				num = 1
				openEnds = 2
				for r in range(1,6):
					if self.position( (move[0]+r*direction[0], move[1]+r*direction[1]) ) == player:
						num += 1
					else:
						if self.position( (move[0]+r*direction[0], move[1]+r*direction[1]) ) == 1-player:
							openEnds -= 1
						break
				for r in range(1,6):
					if self.position( (move[0]-r*direction[0], move[1]-r*direction[1]) ) == player:
						num += 1
					else:
						if self.position( (move[0]-r*direction[0], move[1]-r*direction[1]) ) == 1-player:
							openEnds -= 1
						break

				if openEnds == 2:
					openEnded[player][min(5,num)] += 1
				if openEnds == 1:
					halfOpenEnded[player][min(5,num)] += 1
			
		return openEnded, halfOpenEnded


