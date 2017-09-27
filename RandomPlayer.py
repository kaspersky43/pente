from Player import *
from random import *

class MyPlayer(Player):
	
	def __init__(self, position, visualizer=None):
		Player.__init__(self, position)
		
	def calculateMove(self, position):
		candidates = []
		for r in range(19):
			for c in range(19):
				if position.legalMove((r,c)):
					candidates.append((r,c))
		shuffle(candidates)
		return candidates[0]
