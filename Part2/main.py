import sys, os, math, time
from minimax_agent import *
from alphabeta_agent import *
from state import *

defaultBoard = [[2, 2, 2, 2, 2, 2, 2, 2],
				[2, 2, 2, 2, 2, 2, 2, 2],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[1, 1, 1, 1, 1, 1, 1, 1],
				[1, 1, 1, 1, 1, 1, 1, 1]]

def minimaxGame1():
	btBoard = state.State()
