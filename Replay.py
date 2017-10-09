from argparse import *
from time import *

from Pente import *
from DrawPente import *

parser = ArgumentParser(description="Play Pente locally")
parser.add_argument("moves", help="string representation of the move sequence")
parser.add_argument("time", help="time for each move (0 to wait for user input)", type=int)
parser.add_argument("-g", help="scale for the graphics rendering", dest="scale", action="store", type=int)
args = parser.parse_args()

if args.scale:
	graphics = DrawPente(args.scale, False)
else:
	graphics = None
	
moves = args.moves
waitTime = args.time

position = Pente()

for i in range(0,len(moves),2):
	move = (ord(moves[i])-65, ord(moves[i+1])-65)
	position = position.applyMove(move)
	
	position.display()
	print
	
	if graphics:
		graphics.draw(position)
		
	if waitTime > 0:
		sleep(waitTime)
	else:
		raw_input('Hit enter to continue')
		print

