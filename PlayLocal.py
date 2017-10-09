from argparse import *
from time import *

from Pente import *
from DrawPente import *
from Timeout import *

parser = ArgumentParser(description="Play Pente locally")
parser.add_argument("player1", help="filename for first player")
parser.add_argument("player2", help="filename for second player")
parser.add_argument("timelimit", help="maximum time for each move")
parser.add_argument("-g", help="scale for the graphics rendering", dest="scale", action="store", type=int)
parser.add_argument("-o", help="display options as an agent thinks", action="store_true", dest="options", default=False)
args = parser.parse_args()

player1 = '.'.join(args.player1.split('.')[:-1])
player2 = '.'.join(args.player2.split('.')[:-1])

exec('from %s import MyPlayer as MyPlayer1' % player1)
exec('from %s import MyPlayer as MyPlayer2' % player2)

timelimit = int(args.timelimit)

if args.scale:
	graphics = DrawPente(args.scale, args.options)
else:
	graphics = None

players = [MyPlayer1(0, graphics), MyPlayer2(1, graphics)]
position = Pente()

@timeout(timelimit)
def getMove(current,position):
	return players[current].calculateMove(position)


moveSequence = ''

numMoves = [0,0]
ply = [0.,0.]
nodeCount = [0,0]
totalTime = [0.,0.]

while position.winner() is None:
	position.display()
	if graphics:
		graphics.draw(position)
	
	current = position.playerToMove()
	startTime = time()
	move = getMove(current,position)
	elapsed = time() - startTime

	print
	print ['White','Black'][current], 'move at row', move[0], 'column', move[1]
	print elapsed, 'seconds to find the move'
	print
	
	moveSequence += chr(65+move[0]) + chr(65+move[1])
	
	if position.turn() >= 3:
		numMoves[current] += 1
		ply[current] += players[current]._ply
		nodeCount[current] += players[current]._nodeCount
		totalTime[current] += elapsed
	
	if position.legalMove(move):
		players[1-current].opponentMove(move)
		position = position.applyMove(move)
	else:
		print 'Player', current, 'illegal move!'
		break

	
position.display()
if graphics:
	graphics.draw(position)
	
for i in range(2):
	print
	print 'Player', i, 'stats:'
	print '     Average ply', ply[i]/numMoves[i]
	print '     Nodes/sec', nodeCount[i]/totalTime[i]
	print '     Branching factor', (nodeCount[i]/numMoves[i])**(numMoves[i]/ply[i])


print
print 'Move sequence:'
print moveSequence
