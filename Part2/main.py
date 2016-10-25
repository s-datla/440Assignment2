import sys, os, math, time
from minimax_agent import *
from alphabeta_agent import *
from state import *

OFFENSIVE = 1
DEFENSIVE = 0

RESUME = 0

def minimaxGame1():
	btBoard = state.State(False)

	whiteMinimax = minimax_agent.Minimax(OFFENSIVE)
	blackMinimax = minimax_agent.Minimax(DEFENSIVE)

	totalNumMoves = 0
	blackMoveTime = 0
	whiteMoveTime = 0
	whiteMoves = 0
	blackMoves = 0

	print "Starting Game \n"

	while True:
		whiteStartTime = time.time()

		whiteMinimax.buildTree(btBoard, 1, 3)
		nextMove = whiteMinimax.minimaxValue(3)[1]
		btBoard.transition(nextMove[0], 1, nextMove[1])

		whiteEndTime = time.time()
		whiteMoveTime = abs(whiteEndTime - whiteStartTime)
		whiteMoves += 1

		if btBoard.endGame() != RESUME:
			break

		blackStartTime = time.time()

		blackMinimax.buildTree(btBoard, -1, 3)
		nextMove = blackMinimax.minimaxValue(3)[1]
		btBoard.transition(nextMove[0], -1, nextMove[1])

		blackEndTime = time.time()
		blackMoveTime = abs(blackEndTime - blackStartTime)
		blackMoves += 1

		if btBoard.endGame() != RESUME:
			break

		btBoard.printBoard()
	print "-" * 20

	btBoard.printBoard()

	avgWhiteMoveTime = whiteMoveTime / whiteMoves
	avgBlackMoveTime = blackMoveTime / blackMoves

	avgWhiteNodes = whiteMinimax.numExpandedNodes / whiteMoves
	avgBlackNodes = blackMinimax.numExpandedNodes / blackMoves

	print "White Stats: \n"
	print "Average time per move: " + str(avgWhiteMoveTime) + " sec"
	print "Number of moves before game end: " + str(whiteMoves)
	print "Average number of expanded nodes per move: " + str(avgWhiteNodes)
	print "Total number of nodes expanded in game: " + str(whiteMinimax.numExpandedNodes)

	print "\nBlack Stats: \n"
	print "Average time per move: " + str(avgBlackMoveTime) + " sec"
	print "Number of moves before game end: " + str(blackMoves)
	print "Average number of expanded nodes per move: " + str(avgBlackNodes)
	print "Total number of nodes expanded in game: " + str(blackMinimax.numExpandedNodes)

minimaxGame1()