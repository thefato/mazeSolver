import pygame
import random

CELL_WIDTH = 20
CELL_HEIGHT = 20
NUM_CELLS = 21
WIDTH = NUM_CELLS * CELL_WIDTH
HEIGHT = NUM_CELLS * CELL_HEIGHT
WALL_COLOR = (0, 0, 0) # preto
PATH_COLOR = (255, 255, 255) # branco
ENTRY_COLOR = (0, 0, 255) # azul
EXIT_COLOR = (255, 0, 0) # vermelho
PATH_TRAVERSED_COLOR = (255, 105, 180) # rosa
FINAL_PATH_COLOR = (0, 255, 0) # verde
ERROR_PATH_COLOR = (255, 0, 0) # vermelho
MESSAGE_COLOR = (255, 255, 0) # amarelo
FPS=30

class Maze:
    def __init__(self, height, width, error_chance=0.2):
        self.height = height
        self.width = width
        self.error_chance = error_chance
        self.maze = self.create_maze() #chama a função de criar labirinto

    def create_maze(self):
        maze = [[1 for _ in range(self.width)] for _ in range(self.height)]  # Cria um labirinto cheio de paredes (1)
        self.carve_path(random.randrange(1, self.height, 2), random.randrange(1, self.width, 2), maze) # Chama a função de furar o caminho no labirinto

        if random.random() < self.error_chance: # Adiciona um erro aleatório no labirinto 
            if random.choice([True, False]): 
                maze[1][0] = 1
            else: 
                maze[self.height - 2][self.width - 1] = 1
        else:
            maze[1][0] = 0
            maze[self.height - 2][self.width - 1] = 0
        return maze

    def carve_path(self, row, col, maze): # Função que fura o caminho no labirinto
        maze[row][col] = 0 # Marca a célula atual como caminho (0)
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)] # Direções possíveis (cima, baixo, esquerda, direita)
        random.shuffle(directions) # Embaralha as direções para criar um labirinto aleatório

        for dr, dc in directions: # Para cada direção
            new_row, new_col = row + 2 * dr, col + 2 * dc # Calcula a nova posição
            if 0 < new_row < self.height - 1 and 0 < new_col < self.width - 1 and maze[new_row][new_col] == 1: # Verifica se a nova posição está dentro dos limites e é uma parede (1)
                maze[row + dr][col + dc] = 0 # Marca a célula entre a atual e a nova posição como caminho (0)
                self.carve_path(new_row, new_col, maze) # Chama recursivamente a função para continuar furando o caminho

class PathFinder: 
    def __init__(self, maze): # Inicializa o caminho
        self.maze = maze # Labirinto
        self.width = len(maze[0]) # Largura do labirinto
        self.height = len(maze) # Altura do labirinto

    def find_path(self, entry, exit): # Encontra o caminho entre a entrada e a saída
        queue = [(entry, [])] # Fila para armazenar as posições a serem exploradas e o caminho até elas
        visited = set() # Conjunto para armazenar as posições já visitadas
        explored = [] # Lista para armazenar as posições exploradas

        while queue: # Enquanto houver posições na fila
            (row, col), path = queue.pop(0) # Remove a primeira posição da fila
            if (row, col) in visited: # Se a posição já foi visitada, ignora
                continue
            visited.add((row, col)) # Marca a posição como visitada
            explored.append((row, col)) # Adiciona a posição à lista de exploradas

            if (row, col) == exit:
                return path + [(row, col)], explored # Se a posição atual for a saída, retorna o caminho e as posições exploradas

            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]: # Direções possíveis (cima, baixo, esquerda, direita)
                new_row, new_col = row + dr, col + dc # Calcula a nova posição
                if 0 <= new_row < self.height and 0 <= new_col < self.width: # Verifica se a nova posição está dentro dos limites
                    if self.maze[new_row][new_col] == 0 and (new_row, new_col) not in visited: # Se a nova posição for um caminho (0) e não foi visitada
                        queue.append(((new_row, new_col), path + [(row, col)])) # Adiciona a nova posição à fila com o caminho até ela

        return [], explored

class Drawer: 
    def __init__(self, screen): # Inicializa o objeto de desenho
        self.screen = screen # Tela do Pygame

    def draw_maze(self, maze, path, explored, entry, exit, no_solution): # Desenha o labirinto na tela
        for row in range(len(maze)): # Para cada linha do labirinto
            for col in range(len(maze[0])): # Para cada coluna do labirinto
                x = col * CELL_WIDTH # Calcula a posição x
                y = row * CELL_HEIGHT # Calcula a posição y
                color = PATH_COLOR if maze[row][col] == 0 else WALL_COLOR # Define a cor da célula (caminho ou parede)
                pygame.draw.rect(self.screen, color, (x, y, CELL_WIDTH, CELL_HEIGHT)) # Desenha a célula na tela

        if no_solution: # Se não houver solução
            for row, col in explored: # Para cada posição explorada
                x = col * CELL_WIDTH # Calcula a posição x
                y = row * CELL_HEIGHT # Calcula a posição y
                pygame.draw.rect(self.screen, ERROR_PATH_COLOR, (x, y, CELL_WIDTH, CELL_HEIGHT)) # Desenha as células exploradas em vermelho
        else: # Se houver solução
            for row, col in explored: # Para cada posição explorada
                x = col * CELL_WIDTH # Calcula a posição x
                y = row * CELL_HEIGHT # Calcula a posição y
                pygame.draw.rect(self.screen, PATH_TRAVERSED_COLOR, (x, y, CELL_WIDTH, CELL_HEIGHT)) # Desenha as células exploradas em rosa

            for row, col in path: # Para cada posição do caminho
                x = col * CELL_WIDTH # Calcula a posição x
                y = row * CELL_HEIGHT # Calcula a posição y
                pygame.draw.rect(self.screen, FINAL_PATH_COLOR, (x, y, CELL_WIDTH, CELL_HEIGHT)) # Desenha o caminho em verde/solução final

        pygame.draw.rect(self.screen, ENTRY_COLOR, (entry[1] * CELL_WIDTH, entry[0] * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT)) # Desenha a entrada em azul
        pygame.draw.rect(self.screen, EXIT_COLOR, (exit[1] * CELL_WIDTH, exit[0] * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT)) # Desenha a saída em vermelho

        if no_solution: # Se não houver solução
            font = pygame.font.Font(None, 36)
            text = font.render("Nenhuma solução encontrada.", True, MESSAGE_COLOR) # Renderiza a mensagem
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            self.screen.blit(text, text_rect)

class Main:
    def __init__(self): # Inicializa o objeto principal
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("21x21 Maze")
        self.clock = pygame.time.Clock()

    def start(self): # Inicia o jogo
        maze_obj = Maze(NUM_CELLS, NUM_CELLS)
        pathfinder_obj = PathFinder(maze_obj.maze)
        drawer_obj = Drawer(self.screen)

        entry = (1, 0)
        exit = (NUM_CELLS - 2, NUM_CELLS - 1)

        path, explored = pathfinder_obj.find_path(entry, exit)
        no_solution = not path

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill(PATH_COLOR)
            drawer_obj.draw_maze(maze_obj.maze, path, explored, entry, exit, no_solution)
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()

app = Main()
app.start()