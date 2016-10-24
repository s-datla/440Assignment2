import state

OFFENSIVE = 1
DEFENSIVE = 0

WHITE = -1
BLACK = 1

def evaluateFunction(currentBoard, newBoard, turn, heuristic):
	utility = 0

	if turn == WHITE:
			attacker = self.whitePositions
			defender = self.blackPositions
		else:
			attacker = self.blackPositions
			defender = self.whitePositions

	if heuristic == OFFENSIVE:
		utility += useOffensive(currentBoard, newBoard, turn)
	elif heuristic == DEFENSIVE:
		utility += useDefensive(currentBoard, newBoard, turn)

	return utility

def useOffensive(currentBoard, newBoard, turn):
	'''
	Calculate pieces lost by current player
	Calculate those with further progress
	Check for pieces in danger and pieces which are safe

	Tiebreaker to those further ahead to move
	Lost pieces and captured pieces have a value
	'''