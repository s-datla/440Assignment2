import heuristics
import state

maxNum = float("inf")
minNum = -float("inf")

INVALID = -1
VALID = 1

LEFT = 0
FORWARD = 1
RIGHT = 2

CAPTURE = 3
WINCONDITION = 30

#  Minimax class: Meant to build a tree instance of Minimax before selecting optimal value for given depth
class Minimax:
	# Class constructor.  Meant to indicate heuristic used for evaluation
	def __init__(self, heuristic):
		self.root = None
		self.turn = None
		self.numExpandedNodes = 0
		self.heuristic = heuristic

	# Individual nodes of the minimax tree.
	# Stores details about each specific piece, directions taken to reach this point and its children 
	class minimaxNode:
		value = None
		def __init__(self, pieceID, moveVal):
			self.pieceID = pieceID
			self.direction = moveVal
			self.children = []

	# To be used for building the initial Minimax tree
	def buildTree(self, boardState, turn, depth):
		self.turn = turn
		self.root = self.buildTreeSecondary(boardState, turn, depth, None, None)

	# Secondary function that acts as the recursive base case for building a Minimax tree.
	# 
	def buildTreeSecondary(self, currentBoard, turn, depth, piece, direction):
		if depth == 0:
			retVal = self.minimaxNode(piece, direction)
			retVal.value = # Heuristic evaluation function
			return retVal

		newNode = self.minimaxNode(piece, direction)

		for i in range(currentBoard.size * 2):
			for move in [LEFT, FORWARD, RIGHT]:
				result = currentBoard.validAction(i, turn, move)
				if result == INVALID:
					continue

				newBoard = currentBoard.deepCopy()
				newBoard.transition(i, turn, move)

				childNode = self.buildTreeSecondary(newBoard, -1 * turn, depth - 1, i, move)
				newNode.children.append(childNode)
				self.numExpandedNodes += 1
		return newNode

	# Used to retrieve best move available based on the Minimax Tree
	def minimaxValue(self, depth):
		childMax = minNum
		move = (None, None)
		for child in self.root.children:
			result = self.minimaxValueSecondary(child, depth - 1)
			if result > childMax:
				childMax = result
				move = (child.pieceID, child.direction)
		self.root.value = childMax
		return [childMax, move]

	# Similarly to generating the tree, secondary function  that acts as a recursive base case for selecting the best move in the Minimax tree
	def minimaxValueSecondary(self, currentNode, depth):
		if depth == 0:
			return currentNode.value

		if depth % 2 == 1:
			childMax = minNum

			for child in currentNode.children:
				result = self.minimaxValueSecondary(child, depth - 1)
				if result > childMax:
					childMax = result

			currentNode.value = childMax
			return childMax
		else:
			childMax = maxNum

			for child in currentNode.children:
				result = self.minimaxValueSecondary(child, depth - 1)
				if result < childMax:
					childMax = result

			currentNode.value = childMax
			return childMax