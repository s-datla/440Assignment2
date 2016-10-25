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

class Minimax:
	def __init__(self, heuristic):
		self.root = None
		self.currentBoard = None
		self.turn = None
		self.numExpandedNodes = 0
		self.heuristic = heuristic

	class minimaxNode:
		value = None
		def __init__(self, pieceID, moveVal):
			self.pieceID = pieceID
			self.direction = moveVal
			self.children = []

	def buildTree(self, boardState, turn, depth):
		self.turn = turn
		self.currentBoard = boardState
		self.root = self.buildTreeSecondary(boardState, turn, depth, None, None)

	def buildTreeSecondary(self, currentBoard, turn, depth, piece, direction):
		if depth == 0:
			retVal = self.minimaxNode(piece, direction)
			retVal.value = heuristics.evaluateFunction(self.currentBoard, currentBoard, self.turn, self.heuristic)
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