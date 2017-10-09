from Player import *
from Timeout import *

from random import *

from DrawPente import *

class MyPlayer(Player):
	
	def __init__(self, playerID, visualizer=None):
		Player.__init__(self, playerID)
		self._draw = visualizer

	def calculateMove(self, position):
		try:
			bestMove = None
			movesConsidered = []
			depth = 4
			self._nodeCount = 0
			if self.playerID() == 0:
				# The max player
				bestValue = -(1<<64)
				alpha = -(1<<64)
				beta = 1<<64
				options = self.orderMoves(position)
				if self._draw:
					self._draw.drawOptions(position, [], None, bestValue, len(options), depth)
				print
				print 'Max player'
				for o in options:
					if bestMove is None:
						bestMove = o
					movesConsidered.append(o)
					print 'Examining move option', o, 'priority =', self.movePriority(position,o),
					optionValue = self.minPlayer(position.applyMove(o), depth, alpha, beta)
					if optionValue > bestValue:
						bestValue = optionValue
						bestMove = o
						alpha = bestValue
					if self._draw:
						self._draw.drawOptions(position, movesConsidered, bestMove, bestValue, (self._nodeCount*len(options)/len(movesConsidered))**(1./depth), depth)
					print 'value =', optionValue, 'best value = ', bestValue
			else:
				# The min player
				bestValue = 1<<64
				alpha = -(1<<64)
				beta = 1<<64
				options = self.orderMoves(position)
				if self._draw:
					self._draw.drawOptions(position, [], None, bestValue, len(options), depth)
				print
				print 'Min player'
				oe = []
				for o in options:
					if bestMove is None:
						bestMove = o
					movesConsidered.append(o)
					print 'Examining move option', o, 'priority =', self.movePriority(position,o),
					optionValue = self.maxPlayer(position.applyMove(o), depth, alpha, beta)
					if optionValue < bestValue:
						bestValue = optionValue
						bestMove = o
						beta = bestValue
					if self._draw:
						self._draw.drawOptions(position, movesConsidered, bestMove, bestValue, (self._nodeCount*len(options)/len(movesConsidered))**(1./depth), depth)
					print 'value =', optionValue, 'best value = ', bestValue
		except TimeoutError:
			print
			print 'Timeout'
		
		print
		print self._nodeCount, 'nodes examined'
		self._ply = depth - 1 + float(len(movesConsidered))/len(options)	
		return bestMove
		
	def maxPlayer(self, position, depth, alpha, beta):
		self._nodeCount += 1
		if position.winner() is not None:
			if position.winner() == 0:
				value = 1<<32
			elif position.winner() == 1:
				value = -(1<<32)
			else:
				value = 0
				
			return value
		if depth == 0:
			return self.heuristic(position)
			
		bestValue = -float('inf')
		for o in self.orderMoves(position):
			optionValue = self.minPlayer(position.applyMove(o), depth-1, alpha, beta)
			if optionValue > bestValue:
				bestValue = optionValue
				if bestValue >= beta:
					return bestValue
				alpha = max(alpha, bestValue)
				
		return bestValue
		
	def minPlayer(self, position, depth, alpha, beta):
		self._nodeCount += 1
		if depth == 0:
			return self.heuristic(position)
		if position.winner() is not None:
			if position.winner() == 0:
				value = 1<<32
			elif position.winner() == 1:
				value = -(1<<32)
			else:
				value = 0
				
			return value
			
		bestValue = float('inf')
		for o in self.orderMoves(position):
			optionValue = self.maxPlayer(position.applyMove(o), depth-1, alpha, beta)
			if optionValue <= bestValue:
				bestValue = optionValue
				if bestValue <= alpha:
					return bestValue
				beta = min(beta, bestValue)
				
		return bestValue
		
	
		
	def selectMoves(self, position):
		if position.turn() == 1:
			return [(9,9)]		
		
		occupied = position._positions[0] | position._positions[1]
		current = 0L
		for direction in [(0,1),(1,0),(1,1),(1,-1)]:
			for dist in range(1,4):
				shift = (19*direction[0] + direction[1])*dist
				
				current |= occupied << shift
				current |= occupied >> shift	
		
		
		moves = []
		for i in range(361):
			if current & (1 << i) > 0 and position.legalMove((i/19,i%19)):
				moves.append( (i/19,i%19) )
		
		return moves
		
	def orderMoves(self, position):
		options = []
		for m in self.selectMoves(position):
			options.append( (self.movePriority(position,m), random(), m) )
		options.sort()
		options.reverse()
		
		return [ x[2] for x in options ][:20]
		
	def movePriority(self, position, move):
		openEnded, halfOpenEnded = position.evaluateMove(move)
		
		score = 0
		for p in range(2):
			score += 100*position.isFiveInARow(move, p)
			score += 20*position.isCapture(move, p)
			for l in range(1,6):
				score += l*openEnded[p][l]
				score += l*halfOpenEnded[p][l]
			
		return score
		
	def heuristic(self, position):
		h = 10000*position.patternCount('WWWWW') - 10000*position.patternCount('BBBBB')
		h += 1000*position.captures()[0] - 1000*position.captures()[1]

                #Create 4 stones and 3 stones crossing each other so that the player can use it to push force to the attack
                h += 500*(position.patternCount(' WW W ') + position.patternCount('W  W') - position.patternCount(' BB B ') - position.patternCount('B  B'))
                h += 500*(position.patternCount(' WW W ') + position.patternCount('W W') - position.patternCount(' BB B ') - position.patternCount('B B'))
                h += 500*(position.patternCount(' WW W ') + position.patternCount('WW  ') - position.patternCount(' BB B ') - position.patternCount('BB  '))
                h += 500*(position.patternCount('W W W') + position.patternCount('W  W') - position.patternCount('B B B') - position.patternCount('B  B'))
                h += 500*(position.patternCount(' W W ') + position.patternCount('WW  W') + position.patternCount('WW ') - position.patternCount(' B B ') - position.patternCount('BB  B') - position.patternCount('BB '))
                h += 500*(position.patternCount('W W W') + position.patternCount('WW   ') + position.patternCount('W W') - position.patternCount('B B B') - position.patternCount('BB   ') - position.patternCount('B B'))


                h += 30*(position.patternCount('WWWW') - position.patternCount('BBBB'))
		h += 20*(position.patternCount('WWW') - position.patternCount('BBB'))               
                
		h += 10*(position.patternCount('WW') - position.patternCount('BB'))
		return h
