class Player:
	"""Abstract base class for a Pente player."""
	
	def __init__(self, playerID, visualizer=None):
		"""Initialize the player.  playerID is either 0 or 1 with 0 first to move."""
		self._playerID = playerID
		
	def playerID(self):
		"""Return which position the player is in."""
		return self._playerID
		
	def opponentMove(self, move):
		"""Reports on the move made by the oppenent."""
		pass
		
	def calculateMove(self, position):
		"""Determine the move the player is making."""
		pass
