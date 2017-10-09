from Pente import *
from cs1graphics import *

class DrawPente:
	def __init__(self, scale, showOptions):
		self._scale = scale
		self._showOptions = showOptions
		if showOptions:
			self._canvas = Canvas(scale*31.5, scale*21.5)
		else:
			self._canvas = Canvas(scale*21, scale*21.5)
			
		self._renderedLarge = set()
		self._renderedSmall = [ set(), set() ]
			
		self._canvas.setAutoRefresh(False)
		self._canvas.setBackgroundColor('tan')
		
		self._turn = Text('Turn: 1', .9*scale, Point(scale*21*.15, scale*.5))
		self._canvas.add(self._turn)
		self._message = Text('White to move', .9*scale, Point(scale*21*.45, scale*.5))
		self._canvas.add(self._message)
		self._captures = Text('Captures: 0 0', .9*scale, Point(scale*21*.8, scale*.5))
		self._canvas.add(self._captures)
		
		for i in range(19):
			p = Path([Point(scale*(i+1.5),2*scale), Point(scale*(i+1.5),21*scale)])
			p.setDepth(100)
			self._canvas.add(p)
			p = Path([Point(scale,scale*(i+2.5)), Point(20*scale,scale*(i+2.5))])
			p.setDepth(100)
			self._canvas.add(p)
			
			self._canvas.add( Text('%d' % i, .9*scale, Point(scale*.5, scale*(i+2.5))) )
			self._canvas.add( Text('%d' % i, .9*scale, Point(scale*(i+1.5), scale*1.5)) )
		
		self._pieces = []
		for r in range(19):
			l = []
			for c in range(19):
				l.append(Circle(.45*scale, Point((c+1.5)*scale,(r+2.5)*scale)))
			self._pieces.append(l)
			
		# For each of the options boards do more
		self._plys = []
		self._ebfs = []
		self._values = []
		self._optionPieces = []
		for player in range(2):
			self._optionPieces.append([])
			for i in range(19):
				p = Path([Point((21.75+.5*i)*scale,(1+10.5*player)*scale), Point((21.75+.5*i)*scale, (10.5+10.5*player)*scale)])
				p.setDepth(100)
				self._canvas.add(p)
				p = Path([Point(21.5*scale, (1.25+10.5*player+.5*i)*scale), Point(31*scale, (1.25+10.5*player+.5*i)*scale)])
				p.setDepth(100)
				self._canvas.add(p)
				
			self._plys.append(Text(['White  Ply 0', 'Black  Ply 0'][player], .6*scale, Point(23*scale, .5*scale + 10.5*player*scale)))
			self._canvas.add(self._plys[player])
			self._ebfs.append(Text('EBF: ?', .6*scale, Point(26.5*scale, .5*scale + 10.5*player*scale)))
			self._canvas.add(self._ebfs[player])
			if player == 0:
				self._values.append(Text("-Infinity", .6*scale, Point(30*scale, .5*scale + 10.5*player*scale)))
			else:
				self._values.append(Text("Infinity", .6*scale, Point(30*scale, .5*scale + 10.5*player*scale)))
			self._canvas.add(self._values[player])
			
			for r in range(19):
				l = []
				for c in range(19):
					l.append(Circle(.225*scale, Point((.5*c+21.75)*scale,(1.25+10.5*player+.5*r)*scale)))
				self._optionPieces[player].append(l)
			
		self._canvas.refresh()
		
	def draw(self, position):
		self._turn.setMessage('Turn %d' % position.turn())
		if position.winner() is None:
			self._message.setMessage(['White','Black'][position.playerToMove()] + ' to move')
		else:
			self._message.setMessage(['White','Black'][position.winner()] + ' won')
		self._captures.setMessage('Captures: %d %d' % (position.captures()[0],position.captures()[1]))
	
		s = bin(position._positions[0] | position._positions[1])[2:][::-1]
		l = [ i for i in range(len(s)) if s[i] == '1' ]
		toBeRendered = set( [ (i/19, i%19) for i in l ] )
		
		for (r,c) in self._renderedLarge - toBeRendered:
			self._canvas.remove(self._pieces[r][c])
			
		for (r,c) in toBeRendered - self._renderedLarge:
			self._canvas.add(self._pieces[r][c])
			
		for (r,c) in toBeRendered:
				p = position.position((r,c))
				if p == 0:
					self._pieces[r][c].setFillColor('white')
				elif p == 1:
					self._pieces[r][c].setFillColor('black')
					
		self._renderedLarge = toBeRendered
				
		self._canvas.refresh()

	def drawOptions(self, position, movesConsidered, bestMove, bestValue, ebf, depth):
		options = set(movesConsidered)
		if bestMove:
			options.add(bestMove)
		player = position.playerToMove()
		
		s = bin(position._positions[0] | position._positions[1])[2:][::-1]
		l = [ i for i in range(len(s)) if s[i] == '1' ]
		toBeRendered = set( [ (i/19, i%19) for i in l ] )
		
		for m in movesConsidered:
			toBeRendered.add(m)
		if bestMove is not None:
			toBeRendered.add(bestMove)
		
		for (r,c) in self._renderedSmall[player] - toBeRendered:
			self._canvas.remove(self._optionPieces[player][r][c])
		for (r,c) in toBeRendered - self._renderedSmall[player]:
			self._canvas.add(self._optionPieces[player][r][c])
		
		for (r,c) in toBeRendered:
			p = position.position((r,c))
			if p == 0:
				self._optionPieces[player][r][c].setFillColor('white')
			elif p == 1:
				self._optionPieces[player][r][c].setFillColor('black')
			
		for (r,c) in options:
			self._optionPieces[player][r][c].setFillColor('red')
				
		if bestMove is not None:		
			(r,c) = bestMove
			self._optionPieces[player][r][c].setFillColor('green')
		
		self._plys[player].setMessage(['White  Ply %d', 'Black  Ply %d'][player]%depth)
		if bestValue > (1<<31):			
			self._values[player].setMessage("Infinity")
		elif bestValue < -(1<<31):			
			self._values[player].setMessage("-Infinity")
		else:
			self._values[player].setMessage(str(bestValue))
		self._ebfs[player].setMessage('EBF: %6.3f' % ebf)
		
		self._renderedSmall[player] = toBeRendered
		
		self._canvas.refresh()
