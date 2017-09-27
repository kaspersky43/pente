from Player import *
from Timeout import *

from random import *

class MyPlayer(Player):
	
	def __init__(self, position, visualizer=None):
		Player.__init__(self, position)
		
	def calculateMove(self, position):
		while True:
			try:
				l = raw_input('Enter the move: ').split()
				r = int(l[0])
				c = int(l[1])
				if position.legalMove((r,c)):
					return (r,c)
				else:
					print 'Invalid'
			except TimeoutError:
				pass
