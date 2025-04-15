import pygame
import random
import heapq

CELL_WIDTH = 20
CELL_HEIGHT = 20
NUM_CELLS = 21
WIDTH = NUM_CELLS * CELL_WIDTH
HEIGHT = NUM_CELLS * CELL_HEIGHT
WALL_COLOR = (0, 0, 0)
PATH_COLOR = (255, 255, 255)
ENTRY_COLOR = (0, 255, 0)
EXIT_COLOR = (0, 0, 255)
PATH_TRAVERSED_COLOR = (255, 105, 180)
FINAL_PATH_COLOR = (0, 255, 0)
ERROR_PATH_COLOR = (255, 0, 0)
MESSAGE_COLOR = (255, 255, 0)
FPS = 30


class Maze:
    def __init__(self, height, width, error_chance=0.2):
        self.height = height
        self.width = width
        self.error_chance = error_chance
        self.maze = self.create_maze()

    def create_maze(self):
        maze = [[1 for _ in range(self.width)] for _ in range(self.height)]
        self.carve_path(random.randrange(1, self.height, 2), random.randrange(1, self.width, 2), maze)

        if random.random() < self.error_chance:
            if random.choice([True, False]):
                maze[1][0] = 1
            else:
                maze[self.height - 2][self.width - 1] = 1
        else:
            maze[1][0] = 0
            maze[self.height - 2][self.width - 1] = 0
        return maze

    def carve_path(self, row, col, maze):
        maze[row][col] = 0
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(directions)

        for dr, dc in directions:
            new_row, new_col = row + 2 * dr, col + 2 * dc
            if 0 < new_row < self.height - 1 and 0 < new_col < self.width - 1 and maze[new_row][new_col] == 1:
                maze[row + dr][col + dc] = 0
                self.carve_path(new_row, new_col, maze)


class DijkstraSolver:
    def __init__(self, maze):
        self.maze = maze
        self.height = len(maze)
        self.width = len(maze[0])

    def solve(self, entry, exit):
        distance = [[float('inf')] * self.width for _ in range(self.height)]
        distance[entry[0]][entry[1]] = 0

        queue = [(0, entry)]
        previous = [[None] * self.width for _ in range(self.height)]

        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        while queue:
            current_distance, (row, col) = heapq.heappop(queue)

            if (row, col) == exit:
                path = []
                while (row, col) != entry:
                    path.append((row, col))
                    row, col = previous[row][col]
                path.append(entry)
                path.reverse()
                return path, distance, previous

            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc
                if 0 <= new_row < self.height and 0 <= new_col < self.width:
                    if self.maze[new_row][new_col] == 0:  # Can move
                        new_distance = current_distance + 1
                        if new_distance < distance[new_row][new_col]:
                            distance[new_row][new_col] = new_distance
                            previous[new_row][new_col] = (row, col)
                            heapq.heappush(queue, (new_distance, (new_row, new_col)))

        return [], distance, previous


class Drawer:
    def __init__(self, screen):
        self.screen = screen

    def draw_maze(self, maze, path, entry, exit, no_solution):
        for row in range(len(maze)):
            for col in range(len(maze[0])):
                x = col * CELL_WIDTH
                y = row * CELL_HEIGHT
                color = PATH_COLOR if maze[row][col] == 0 else WALL_COLOR
                pygame.draw.rect(self.screen, color, (x, y, CELL_WIDTH, CELL_HEIGHT))

        if no_solution:
            font = pygame.font.Font(None, 36)
            text = font.render("Nenhuma solução encontrada.", True, MESSAGE_COLOR)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            self.screen.blit(text, text_rect)
        else:
            for row, col in path:
                x = col * CELL_WIDTH
                y = row * CELL_HEIGHT
                pygame.draw.rect(self.screen, FINAL_PATH_COLOR, (x, y, CELL_WIDTH, CELL_HEIGHT))

        pygame.draw.rect(self.screen, ENTRY_COLOR,
                         (entry[1] * CELL_WIDTH, entry[0] * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT))
        pygame.draw.rect(self.screen, EXIT_COLOR,
                         (exit[1] * CELL_WIDTH, exit[0] * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT))


class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("21x21 Maze with Dijkstra")
        self.clock = pygame.time.Clock()

    def start(self):
        maze_obj = Maze(NUM_CELLS, NUM_CELLS, error_chance=0.2)
        dijkstra_solver = DijkstraSolver(maze_obj.maze)
        drawer_obj = Drawer(self.screen)

        entry = (1, 0)
        exit = (NUM_CELLS - 2, NUM_CELLS - 1)

        path, _, _ = dijkstra_solver.solve(entry, exit)
        no_solution = not path

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill(PATH_COLOR)
            drawer_obj.draw_maze(maze_obj.maze, path, entry, exit, no_solution)
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()


app = Main()
app.start()