# 1 for White, 2 for Black
defaultBoard = [[2, 2, 2, 2, 2, 2, 2, 2],
				[2, 2, 2, 2, 2, 2, 2, 2],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[1, 1, 1, 1, 1, 1, 1, 1],
				[1, 1, 1, 1, 1, 1, 1, 1]]

maxNum = float("inf")
minNum = -float("inf")

WHITE = -1
BLACK = 1

INVALID = -1
VALID = 1

LEFT = 0
FORWARD = 1
RIGHT = 2

DANGER = -1
NOPE = 0
SAFE = 1

CAPTURE = 3
WINCONDITION = maxNum
RESUME = 0

class State:
	def __init__(self, dCopy = False):
		self.size = 8
		self.whitePositions = {}
		self.blackPositions = {}
		if dCopy == False:
			for i in range (self.size):
				self.whitePositions[i] = (i, self.size - 1)
				self.whitePositions[i + self.size] = (i, self.size - 2)
				self.blackPositions[i] = (i, 0)
				self.blackPositions[i + self.size] = (i, 1)

	def deepCopy(self):
		newBoard = State(True)

		for piece in self.whitePositions:
			newBoard.whitePositions[piece] = self.whitePositions[piece]
		for piece in self.blackPositions:
			newBoard.blackPositions[piece] = self.blackPositions[piece]

		return newBoard

	def validAction(self, pieceID, turn, direction):
		if turn == WHITE:
			attacker = self.whitePositions
			defender = self.blackPositions
		else:
			attacker = self.blackPositions
			defender = self.whitePositions

		# Check not already captured
		if pieceID not in attacker:
			return INVALID

		# Check post-move location
		currentPos = attacker[pieceID]
		if direction == LEFT:
			nextPosition = (currentPos[0] + turn, currentPos[1] + turn)
		elif direction == FORWARD:
			nextPosition = (currentPos[0], currentPos[1] + turn)
		elif direction == RIGHT:
			nextPosition = (currentPos[0] - turn, currentPos[1] + turn)

		if nextPosition[0] < 0 or nextPosition[1] < 0 or nextPosition[0] > (self.size - 1) or nextPosition[1] > (self.size - 1):
			return INVALID		

		for piece in attacker:
			if pieceID == piece:
				continue
			if nextPosition == attacker[piece]:
				return INVALID

		for piece in defender:
			if nextPosition == defender[piece]:
				if not direction == FORWARD:
					return CAPTURE
				else:
					return INVALID

		# Win condition?
		if turn == WHITE and nextPosition[1] == 0:
			return WINCONDITION
		elif turn == BLACK and nextPosition[1] == (self.size - 1):
			return WINCONDITION

		return VALID

	def transition(self, pieceID, turn, direction):
		#print pieceID, direction
		if turn == WHITE:
			attacker = self.whitePositions
			defender = self.blackPositions
		else:
			attacker = self.blackPositions
			defender = self.whitePositions

		if direction == LEFT:
			nextPosition = (attacker[pieceID][0] + turn, attacker[pieceID][1] + turn)
		elif direction == FORWARD:
			nextPosition = (attacker[pieceID][0], attacker[pieceID][1] + turn)
		elif direction == RIGHT:
			nextPosition = (attacker[pieceID][0] - turn, attacker[pieceID][1] + turn)

		attacker[pieceID] = nextPosition
		for piece in defender:
			if defender[piece] == nextPosition:
				del defender[piece]
				break

	def endGame(self):
		if len(self.whitePositions) == 0:
			return BLACK
		elif len(self.blackPositions) == 0:
			return WHITE

		for piece in self.whitePositions:
			if self.whitePositions[piece][1] == 0:
				return WHITE

		for piece in self.blackPositions:
			if self.blackPositions[piece][1] == self.size - 1:
				return BLACK
		return RESUME

	def calcSafeMoves(self, turn):
		if turn == WHITE:
			attacker = self.whitePositions
			defender = self.blackPositions
		else:
			attacker = self.blackPositions
			defender = self.whitePositions

		testBoard = [[NOPE for i in range(self.size)] for j in range(self.size)]
		for piece in attacker:
			currentPos = attacker[piece]
			testBoard[currentPos[1]][currentPos[0]] = SAFE

			for move in [LEFT, FORWARD, RIGHT]:
				if self.validAction(piece, turn, move) != INVALID:
					if move == LEFT:
						nextPosition = (currentPos[0] + turn, currentPos[1] + turn)
					elif move == FORWARD:
						nextPosition = (currentPos[0], currentPos[1] + turn)
					elif move == RIGHT:
						nextPosition = (currentPos[0] - turn, currentPos[1] + turn)

					testBoard[nextPosition[1]][nextPosition[0]] = SAFE

		for piece in defender:
			currentPos = defender[piece]

			for move in [LEFT, FORWARD, RIGHT]:
				if self.validAction(piece, -1 * turn, move) != INVALID:
					if move == LEFT:
						nextPosition = (currentPos[0] + -1 * turn, currentPos[1] + -1 * turn)
					elif move == FORWARD:
						nextPosition = (currentPos[0], currentPos[1] + -1 * turn)
					elif move == RIGHT:
						nextPosition = (currentPos[0] - (-1 * turn), currentPos[1] + -1 * turn)

					testBoard[nextPosition[1]][nextPosition[0]] = DANGER
		totalSafe = 0
		for row in testBoard:
			for spot in row:
				if spot == SAFE:
					totalSafe += 1

		return totalSafe

	def calcEndangeredPieces(self, turn):
		if turn == WHITE:
			attacker = self.whitePositions
			defender = self.blackPositions
		else:
			attacker = self.blackPositions
			defender = self.whitePositions

		testBoard = [[NOPE for i in range(self.size)] for j in range(self.size)]

		for piece in defender:
			currentPos = defender[piece]

			for move in [LEFT, FORWARD, RIGHT]:
				if self.validAction(piece, -1 * turn, move) != INVALID:
					if move == LEFT:
						nextPosition = (currentPos[0] + -1 * turn, currentPos[1] + -1 * turn)
					elif move == FORWARD:
						nextPosition = (currentPos[0], currentPos[1] + -1 * turn)
					elif move == RIGHT:
						nextPosition = (currentPos[0] - -1 * turn, currentPos[1] + -1 * turn)

					testBoard[nextPosition[1]][nextPosition[0]] = DANGER

		totalDanger = 0
		for piece in attacker:
			currentPos = attacker[piece]
			if testBoard[currentPos[1]][currentPos[0]] == DANGER:
				totalDanger += 1

		return totalDanger

	def calcLost(self, currentBoard, turn):
		if turn == WHITE:
			retCalc = (len(self.whitePositions) - len(currentBoard.whitePositions), len(self.blackPositions) - len(currentBoard.blackPositions))
		else:
			retCalc = (len(self.blackPositions) - len(currentBoard.blackPositions), len(self.whitePositions) - len(currentBoard.whitePositions))
		return retCalc

	def furthestPieces(self, turn):
		if turn == WHITE:
			attacker = self.whitePositions
			defender = self.blackPositions
			attackStart = 0
			defenseStart = self.size - 1
		else:
			attacker = self.blackPositions
			defender = self.whitePositions
			attackStart = self.size - 1
			defenseStart = 0

		returnOffense = 0
		for piece in attacker:
			dist = abs(attacker[piece][1] - attackStart) 
			if dist > returnOffense:
				returnOffense = dist

		returnDefense = 0
		for piece in defender:
			dist = abs(defender[piece][1] - defenseStart)
			if dist > returnDefense:
				returnDefense = dist

		return (returnOffense, returnDefense)

	def printBoard(self):
		board = [[' |' for i in range(self.size)] for j in range(self.size)]

		for piece in self.whitePositions:
			currentPos = self.whitePositions[piece]
			board[currentPos[1]][currentPos[0]] = 'w|'

		for piece in self.blackPositions:
			currentPos = self.blackPositions[piece]
			board[currentPos[1]][currentPos[0]] = 'b|'

		print ''.join(['-' for i in range(2 * self.size + 1)])
		for row in range(self.size):
			print '|' + ''.join(board[row])
			print ''.join(['-' for i in range(2 * self.size + 1)])
