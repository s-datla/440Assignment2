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

CAPTURE = 3
WINCONDITION = 30
RESUME = 0

class State:
	def __init__(self, deepCopy = False):
		self.size = 8
		self.whitePositions = {}
		self.blackPositions = {}
		if deepCopy == False:
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
		if direction == LEFT:
			nextPosition = (attacker[pieceID][0] + turn, attacker[pieceID][1] + turn)
		elif direction == FORWARD:
			nextPosition = (attacker[pieceID][0], attacker[pieceID][1] + turn)
		elif direction == RIGHT:
			nextPosition = (attacker[pieceID][0] - turn, attacker[pieceID][1] + turn)

		if nextPosition[0] < 0 or nextPosition[1] < 1 or nextPosition[0] > (self.size - 1) or nextPosition[1] > (self.size - 1):
			return INVALID

		# Win condition?
        if turn == WHITE and nextPosition[1] == 0:
            return WINCONDITION
        elif turn == BLACK and nextPosition[1] == (self.size - 1):
            return WINCONDITION

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

		return VALID

	def transition(self, pieceID, turn, action):
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

	def printBoard(self):
        board = [[' |' for i in range(self.size)] for j in range(self.size)]

        for piece in self.whitePositions:
            curretPos = self.whitePositions[piece]
            board[curretPos[1]][curretPos[0]] = 'w|'

        for piece in self.blackPositions:
            curretPos = self.blackPositions[piece]
            board[curretPos[1]][curretPos[0]] = 'b|'

        print ''.join(['-' for i in range(2 * self.size + 1)])
        for row in range(self.size):
            print '|' + ''.join(board[row])
            print ''.join(['-' for i in range(2 * self.size + 1)])


	def validActions(self):
		validActions = []
		if self.turn == WHITE:
			for position in self.whitePositions:
				if position[0] != 0 and  position[1] != 0 and (position[0] - 1, position[1] - 1) not in self.whitePositions:
					validActions.append(Action(position, 1, WHITE))
				if position[0] != 0 and (position[0] - 1, position[1]) not in self.whitePositions:
					validActions.append(Action(position, 2, WHITE))
				if position[0] != 0 and  position[1] != self.width - 1 and (position[0] - 1, position[1] + 1) not in self.whitePositions:
					validActions.append(Action(position, 3, WHITE))
		elif self.turn == BLACK:
			for position in self.blackPositions:
				if position[0] != self.height - 1 and  position[1] != 0 and (position[0] + 1, position[1] - 1) not in self.blackPositions:
					validActions.append(Action(position, 1, BLACK))
				if position[0] != self.height - 1 and (position[0] + 1, position[1]) not in self.blackPositions:
					validActions.append(Action(position, 2, BLACK))
				if position[0] != self.height - 1 and  position[1] != self.width + 1 and (position[0] + 1, position[1] + 1) not in self.blackPositions:
					validActions.append(Action(position, 3, BLACK))

		return validActions

		def movePiece(coords, direction, turn):
	if turn == WHITE:
		if direction == 1:
			return coords[0] - 1, coords[1] - 1
		elif direction == 2:
			return coords[0] - 1, coords[1]
		elif direction == 3:
			return coords[0] - 1, coords[1] + 1
	elif turn == BLACK:
		if direction == 1:
			return coords[0] + 1, coords[1] - 1
		elif direction == 2:
			return coords[0] + 1, coords[1]
		elif direction == 3:
			return coords[0] + 1, coords[1] + 1

def changeTurn(turn):
	if turn == WHITE:
		return BLACK
	elif turn == BLACK:
		return WHITE

class Action:
	def __init__(self, coords, route, turn):
		self.coords = coords
		self.route = route
		self.turn = turn
	def getActionValues(self):
		return self.coords, self.route, self.turn