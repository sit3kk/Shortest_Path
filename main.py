import pygame
import sys
import collections
import math
from queue import PriorityQueue



pygame.init()
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Shortest Path Algorithms")

RED = (255, 82, 82)
GREEN = (0, 230, 118)
BLUE = (41, 121, 255)
YELLOW = (255, 215 ,0)
WHITE = (238, 233, 200)
BLACK = (18 ,18 ,18)
PURPLE = (156 ,39 ,176)
ORANGE = (255 ,152 ,0)
GREY = (97 ,97 ,97)
TURQUOISE = (0 ,191 ,165)

class Spot:
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = WHITE
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows

	def get_pos(self):
		return self.row, self.col

	def is_closed(self):
		return self.color == RED

	def is_open(self):
		return self.color == GREEN

	def is_barrier(self):
		return self.color == BLACK

	def is_start(self):
		return self.color == ORANGE

	def is_end(self):
		return self.color == TURQUOISE

	def reset(self):
		self.color = WHITE

	def make_start(self):
		self.color = ORANGE

	def make_closed(self):
		self.color = RED

	def make_open(self):
		self.color = GREEN

	def make_barrier(self):
		self.color = BLACK

	def make_end(self):
		self.color = TURQUOISE

	def make_path(self):
		self.color = PURPLE

	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

	def update_neighbors(self, grid):
		self.neighbors = []
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
			self.neighbors.append(grid[self.row + 1][self.col])

		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
			self.neighbors.append(grid[self.row - 1][self.col])

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
			self.neighbors.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
			self.neighbors.append(grid[self.row][self.col - 1])

	def __lt__(self, other):
		return False


def h(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.make_path()
		draw()


def algorithm1(draw, grid, start, end): #A* algorithm
	count = 0
	open_set = PriorityQueue()
	open_set.put((0, count, start)) # Add the start node to the open set with f_score of 0
	came_from = {} # Dictionary to keep track of the path
	g_score = {spot: float("inf") for row in grid for spot in row} # Initialize all g_scores to infinity
	g_score[start] = 0 # Set the g_score of the start node to 0
	f_score = {spot: float("inf") for row in grid for spot in row} # Initialize all f_scores to infinity
	f_score[start] = h(start.get_pos(), end.get_pos()) # Set the f_score of the start node to its heuristic value
 
	open_set_hash = {start} # Set to keep track of nodes in the open set

	while not open_set.empty(): # While there are still nodes to explore
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[2] # Get the node with the lowest f_score from the open set
		open_set_hash.remove(current)

		if current == end: # If we have reached our destination
			reconstruct_path(came_from, end, draw)
			end.make_end()
			return True

		for neighbor in current.neighbors:
			temp_g_score = g_score[current] + 1

			if temp_g_score < g_score[neighbor]:
				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_open()

		draw()

		if current != start:
			current.make_closed()

	return False

def algorithm2(draw, grid, start, end): #Dijkstra
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))  # Add the start node to the open set with distance of 0
    came_from = {} # Dictionary to keep track of the path
    distance = {spot: float("inf") for row in grid for spot in row} # Initialize all distances to infinity
    distance[start] = 0 # Set the distance of the start node to 0

    open_set_hash = {start} # Set to keep track of nodes in the open set

    while not open_set.empty(): # While there are still nodes to explore
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2] # Get the node with the lowest distance from the open set
        open_set_hash.remove(current)

        if current == end:  # If we have reached our destination
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_distance = distance[current] + 1

            if temp_distance < distance[neighbor]:
                came_from[neighbor] = current
                distance[neighbor] = temp_distance
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((distance[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False

def algorithm3(draw, grid, start, end): #BFS
    queue = collections.deque([start]) # Initialize the queue with the start node
    came_from = {} # Dictionary to keep track of the path
    visited = {start} # Set to keep track of visited nodes

    while queue:  # While there are still nodes to explore
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = queue.popleft() # Get the next node from the queue

        if current == end: # If we have reached our destination
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            if neighbor not in visited:
                came_from[neighbor] = current
                queue.append(neighbor)
                visited.add(neighbor)
                neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False

def algorithm4(draw, grid, start, end): #BellmanFord
    distance = {spot: float("inf") for row in grid for spot in row} # Initialize all distances to infinity
    distance[start] = 0 # Set the distance of the start node to 0
    came_from = {} # Dictionary to keep track of the path

    for i in range(len(grid) - 1):
        for spot in [spot for row in grid for spot in row]:
            if distance[spot] != float("inf"):
                for neighbor in spot.neighbors:
                    if distance[spot] + 1 < distance[neighbor]:
                        distance[neighbor] = distance[spot] + 1
                        came_from[neighbor] = spot

    # check for negative cycles
    for spot in [spot for row in grid for spot in row]:
        if distance[spot] != float("inf"):
            for neighbor in spot.neighbors:
                if distance[spot] + 1 < distance[neighbor]:
                    return False

    reconstruct_path(came_from, end, draw)
    end.make_end()
    return True


def make_grid(rows, width):
	grid = []
	gap = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			spot = Spot(i, j, gap, rows)
			grid[i].append(spot)

	return grid

def draw_grid(win, rows, width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
		for j in range(rows):
			pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
	win.fill(WHITE)

	for row in grid:
		for spot in row:
			spot.draw(win)

	draw_grid(win, rows, width)
	pygame.display.update()


def get_clicked_pos(pos, rows, width):
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col


def main(win, width):
	ROWS = 25
	grid = make_grid(ROWS, width) # create a grid with specified number of rows and width

	start = None # initialize start node as None
	end = None # initialize start node as None

	run = True
	while run:
		draw(win, grid, ROWS, width) # draw the grid on the window
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if pygame.mouse.get_pressed()[0]:  # LEFT mouse button pressed 
				pos = pygame.mouse.get_pos()   # get position of mouse click
				row, col = get_clicked_pos(pos, ROWS, width) # get row and column of clicked 
				spot = grid[row][col]
				if not start and spot != end: # if start node is not set and clicked spot is not the end node
					start = spot
					start.make_start() # set start node to clicked spot

				elif not end and spot != start: # if end node is not set and clicked spot is not the start node
					end = spot
					end.make_end()  # set end node to clicked spot

				elif spot != end and spot != start:
					spot.make_barrier() # make barrier at clicked position

			elif pygame.mouse.get_pressed()[2]: # RIGHT mouse button pressed
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				spot.reset() # reset the clicked position to default state (not a barrier)
				if spot == start:
					start = None
				elif spot == end:
					end = None

			if event.type == pygame.KEYDOWN: 
				if event.key == pygame.K_1 and start and end: #A*
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid)
					algorithm1(lambda: draw(win, grid, ROWS, width), grid, start, end)
					
				if event.key == pygame.K_2 and start and end: #Dijkstra
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid)
					algorithm2(lambda: draw(win, grid, ROWS, width), grid, start, end)
					
				if event.key == pygame.K_3 and start and end: #BFS
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid)
					algorithm3(lambda: draw(win, grid, ROWS, width), grid, start, end)
					
				if event.key == pygame.K_4 and start and end: #BellmanFord
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid)
					algorithm4(lambda: draw(win, grid, ROWS, width), grid, start, end)
				
				if event.key == pygame.K_SPACE:
					start = None
					end = None
					grid = make_grid(ROWS, width)

	pygame.quit()
	sys.exit()

main(WIN, WIDTH)