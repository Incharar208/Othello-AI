import pygame
import sys, time, math
import othello

BLOCK_SIZE = 60
PADDING_SIZE = 15
WINDOW_WIDTH = BLOCK_SIZE * 8 
WINDOW_HEIGHT = BLOCK_SIZE * 8 + 20
FRAME_PER_SECOND = 40

class Game_Engine(object):
	def __init__(self):
		super().__init__()
		self.images = {}    # image resources
		self.keys_down = {} # records of down-keys
		
		# create game object
		self.game = othello.Othello()

		self.debug = False # True for debugging

	def preparation(self):
		pygame.init()
		self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
		self.clock = pygame.time.Clock()
		pygame.display.set_caption('Othello')

		# set font
		self.font = pygame.font.SysFont("Helvetica", 56)

		# set images
		self.images['board'] = pygame.image.load('./Images/board.png')
		self.images['board'] = pygame.transform.scale(self.images['board'] ,(WINDOW_WIDTH, WINDOW_HEIGHT))
		self.images['black'] = pygame.image.load('./Images/black.png')
		self.images['white'] = pygame.image.load('./Images/white.png')

		self.drawBoard()

	def newGame(self):
		self.game.__init__()

	def quitGame(self):
		pygame.quit()
		sys.exit()

	def start(self):
		self.preparation()
		self.newGame()

		while True:
			# Check if the AI is ready to make a move
			if self.game.AIReadyToMove:
				self.game.AIMove()  # If ready, let the AI make a move
			else:
				# Handle events
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						self.quitGame()  # Quit the game if the window is closed
					elif event.type == pygame.KEYDOWN:
						self.keydownHandler(event)  # Handle keydown events
					elif event.type == pygame.KEYUP:
						self.keyupHandler(event)  # Handle keyup events
					elif event.type == pygame.MOUSEBUTTONDOWN:
						self.mousedownHandler(event)  # Handle mouse button down events
					elif event.type == pygame.MOUSEBUTTONUP:
						self.mouseupHandler(event)  # Handle mouse button up events
					elif event.type == pygame.MOUSEMOTION:
						self.mousemoveHandler(event)  # Handle mouse motion events

			# Check if the game state has changed
			if self.game.changed:
				self.drawBoard()  # If changed, redraw the board
				self.game.changed = False  # Reset the flag indicating the change

			# Check if the AI is ready to move again
			if self.game.AIReadyToMove:
				self.game.AIMove()  # If ready, let the AI make a move

			self.clock.tick(FRAME_PER_SECOND)  # Control the frame rate of the game

		# Quit the game when the loop exits
		self.quitGame()


	def drawText(self, text, font, screen, x, y, rgb):
		textObj = font.render(text, 1, (rgb[0],rgb[1],rgb[2]))
		textRect = textObj.get_rect()
		textRect.topleft = (x, y)
		screen.blit(textObj, textRect)

	def drawBoard(self):
		# draw the board
		board = pygame.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
		self.screen.blit(self.images['board'], board)

		# draw the menu at the bottom
		menu = pygame.Rect(0, 8 * BLOCK_SIZE, WINDOW_WIDTH, 20)
		pygame.draw.rect(self.screen, (224, 240, 243), menu)
		self.menuFont = pygame.font.SysFont("comicsansms", 15)
		self.drawText("Restart", self.menuFont, self.screen, WINDOW_WIDTH / 2 - 200, 8 * BLOCK_SIZE - 1, (0, 0, 0))
		self.drawText("Exit", self.menuFont, self.screen, WINDOW_WIDTH / 2 + 160, 8 * BLOCK_SIZE - 1, (0, 0, 0))


		# draw blocks and tiles
		for row in range(0, 8):
			for col in range(0, 8):
				block = self.game.board[row][col]
				chessman_size = BLOCK_SIZE - 2 * PADDING_SIZE
				chessman = pygame.Rect(row * BLOCK_SIZE + PADDING_SIZE, col * BLOCK_SIZE + PADDING_SIZE, chessman_size, chessman_size)
				if block == 1:
					self.screen.blit(self.images['black'], chessman)
				elif block == 2:
					self.screen.blit(self.images['white'], chessman)
				elif block == 0:
					pass
				else:
					sys.exit('Error occurs - player number incorrect!')

		self.drawText('Black: ' + str(self.game.blackTiles), self.menuFont, self.screen, WINDOW_WIDTH / 2 - 80, 8 * BLOCK_SIZE - 1, (0, 0, 0))
		self.drawText('White: ' + str(self.game.whiteTiles), self.menuFont, self.screen, WINDOW_WIDTH / 2 + 20, 8 * BLOCK_SIZE - 1, (0, 0, 0))
		
		if self.game.victory in [-1, 1, 2]:
		# Create a rectangle for the game result text
			result_box = pygame.Rect(50, 200, WINDOW_WIDTH - 100, 100)

			# Draw the rectangle for the game result text
			pygame.draw.rect(self.screen, (255, 255, 255), result_box)  # White rectangle
			pygame.draw.rect(self.screen, (0, 0, 0), result_box, 2)  # Black border

			# Draw the game result text inside the rectangle
			result_text = ''
			if self.game.victory == -1:
				result_text = "Draw! " + str(self.game.whiteTiles) + ":" + str(self.game.blackTiles)
			elif self.game.victory == 1:
				if self.game.useAI:
					result_text = "You Won! " + str(self.game.blackTiles) + ":" + str(self.game.whiteTiles)
				else:
					result_text = "Black Won! " + str(self.game.blackTiles) + ":" + str(self.game.whiteTiles)
			elif self.game.victory == 2:
				if self.game.useAI:
					result_text = "AI Won! " + str(self.game.whiteTiles) + ":" + str(self.game.blackTiles)
				else:
					result_text = "White Won! " + str(self.game.whiteTiles) + ":" + str(self.game.blackTiles)

			# Render and draw the result text
			result_font = pygame.font.SysFont("comicsansms", 30)
			result_surface = result_font.render(result_text, True, (0, 0, 0))  # Black text
			result_rect = result_surface.get_rect(center=result_box.center)
			self.screen.blit(result_surface, result_rect.topleft)

		# update display
		pygame.display.update()

	# Definition of Event Handlers
	def keydownHandler(self, event):
		self.keys_down[event.key] = time.time()

	def keyupHandler(self, event):
		if event.key in self.keys_down:
			del(self.keys_down[event.key])

	def mousedownHandler(self, event):
		pass

	def mouseupHandler(self, event):
		x, y = event.pos

		# tested - need to change if window size has been changed
		if x >= 115 and x <= 175 and y >= 8 * BLOCK_SIZE:
			self.newGame()
		elif x >= WINDOW_WIDTH / 2 + 20 and x  <= WINDOW_WIDTH / 2 + 20 + self.menuFont.size("Exit")[0] and y > 8 * BLOCK_SIZE:
			self.quitGame()
		else:
			chessman_x = int(math.floor(x / BLOCK_SIZE))
			chessman_y = int(math.floor(y / BLOCK_SIZE))

			if self.debug:
				print("player " + str(self.game.player) + " x: " + str(chessman_x) + " y: " + str(chessman_y))

			try:
				self.game.playerMove(chessman_x, chessman_y)
				self.game.updateCounts()
			except othello.IllegalMove as e:
				print("Illegal Move " + e.message)
			except Exception as e:
				raise

	def mousemoveHandler(self, event):
		pass

if __name__ == '__main__':
	engine = Game_Engine()
	engine.start()
