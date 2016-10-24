import minimax_agent
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

class AlphaBeta:
	def __init__(self, board, turn, heuristic):
		self.thisMinimax = minimax_agent.Minimax(heuristic)
		self.thisMinimax.buildTree(board, turn, 3)
		self.heuristic = heuristic
		self.numExpandedNodes = 0

	def maxValue(self, node, alpha, beta):
		if len(node.children) == 0:
			return node

		resultNode = minimax_agent.Minimax.minimaxNode(None, None)
		resultNode.value = minNum
		for child in node.children:
			analysedNode = self.minValue(child, alpha, beta)

			if analysedNode.value > resultNode.value:
				resultNode = analysedNode

			if resultNode.value >= beta:
				return resultNode
			alpha = max(alpha, resultNode.value)

		return resultNode

	def minValue(self, node, alpha, beta):
		if len(node.children) == 0:
			return node

		resultNode = minimax_agent.Minimax.minimaxNode(None, None)
		resultNode.value = minNum
		for child in node.children:
			analysedNode = self.maxValue(child, alpha, beta)

			if analysedNode.value < resultNode.value:
				resultNode = analysedNode

			if resultNode.value <= alpha:
				return resultNode
			beta = min(beta, resultNode.value)

		return resultNode

	def alphaBetaSearch(self, node):
		child = self.maxValue(node, minNum, maxNum)
		return [child.pieceID, child.direction]