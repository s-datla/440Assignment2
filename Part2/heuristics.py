import state

OFFENSIVE = 1
DEFENSIVE = 0

WHITE = -1
BLACK = 1

def evaluateFunction(currentBoard, newBoard, turn, heuristic):
	utility = 0

	if turn == WHITE:
		attacker = newBoard.whitePositions
		defender = newBoard.blackPositions
	else:
		attacker = newBoard.blackPositions
		defender = newBoard.whitePositions

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
	heuristic = newBoard.calcSafeMoves(turn)
	#heuristic -= newBoard.calcEndangeredPieces(turn)

	furthestPieces = newBoard.furthestPieces(turn)
	heuristic += furthestPieces[0]
	heuristic -= furthestPieces[1]

	potentialLoss = currentBoard.calcLost(newBoard, turn)
	heuristic += potentialLoss[0] * -1
	heuristic += potentialLoss[1] * 4

	return heuristic

def useDefensive(currentBoard, newBoard, turn):
	heuristic = -newBoard.calcSafeMoves(-1 * turn)
	heuristic -= newBoard.calcEndangeredPieces(turn)

	furthestPieces = newBoard.furthestPieces(turn)
	heuristic += furthestPieces[0]
	heuristic -= furthestPieces[1]

	potentialLoss = currentBoard.calcLost(newBoard, turn)
	heuristic += potentialLoss[0] * -4
	heuristic += potentialLoss[1] * 1

	return heuristic

def checkWinStatus(newBoard, turn):
	