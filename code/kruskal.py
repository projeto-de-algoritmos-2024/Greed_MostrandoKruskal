import pygame
import random
from itertools import combinations

# Configurações iniciais
WIDTH, HEIGHT = 800, 600
NODE_COUNT = 15

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 200, 0)
YELLOW = (255, 255, 0)

# Inicialização do Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Algoritmo de Kruskal")
font = pygame.font.SysFont(None, 30)

nodes = [(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)) for _ in range(NODE_COUNT)]
edges = []


degree = {i: 0 for i in range(NODE_COUNT)}
for (i, n1), (j, n2) in combinations(enumerate(nodes), 2):
    if degree[i] < 4 and degree[j] < 4 and random.random() < 0.5:
        weight = ((n1[0] - n2[0]) ** 2 + (n1[1] - n2[1]) ** 2) ** 0.5
        edges.append((weight, i, j))
        degree[i] += 1
        degree[j] += 1

edges.sort()

def find(parent, i):
    if parent[i] == i:
        return i
    parent[i] = find(parent, parent[i])  # Compressão de caminho
    return parent[i]

def union(parent, rank, x, y):
    root_x = find(parent, x)
    root_y = find(parent, y)
    if rank[root_x] < rank[root_y]:
        parent[root_x] = root_y
    elif rank[root_x] > rank[root_y]:
        parent[root_y] = root_x
    else:
        parent[root_y] = root_x
        rank[root_x] += 1

def kruskal():
    parent = [i for i in range(NODE_COUNT)]
    rank = [0] * NODE_COUNT
    mst = []
    for weight, u, v in edges:
        if find(parent, u) != find(parent, v):
            union(parent, rank, u, v)
            mst.append((weight, u, v))
            yield mst, parent, u, v  

generator = kruskal()
current_mst = []
parent_structure = list(range(NODE_COUNT))
algorithm_started = False
mst_completed = False
show_union_find = False
step_completed = False
current_u, current_v = None, None 

def draw_graph(highlight_edge=None):
    screen.fill(WHITE)
    if not algorithm_started:
        screen.blit(font.render("Pressione ESPAÇO para iniciar", True, BLACK), (WIDTH // 2 - 150, HEIGHT // 2))
    elif mst_completed and not show_union_find:
        for weight, u, v in current_mst:
            pygame.draw.line(screen, RED, nodes[u], nodes[v], 3)
        screen.blit(font.render("Árvore MST encontrada!ENTER para ver a árvore Union-Find", True, BLACK), (WIDTH // 2 - 250, HEIGHT - 50))
    elif show_union_find:
        for i in range(NODE_COUNT):
            root = find(parent_structure, i)
            if i != root:  # Evita desenhar as linhas para os nós que são raízes
                pygame.draw.line(screen, RED, nodes[i], nodes[root], 3)
        screen.blit(font.render("Estrutura Union-Find", True, BLACK), (WIDTH // 2 - 100, HEIGHT - 50))
    else:
        for weight, u, v in edges:
            color = BLACK
            if highlight_edge and (u, v) == highlight_edge or (v, u) == highlight_edge:
                color = YELLOW  # Destaca a aresta considerada
            pygame.draw.line(screen, color, nodes[u], nodes[v], 1)
            mid_x, mid_y = (nodes[u][0] + nodes[v][0]) // 2, (nodes[u][1] + nodes[v][1]) // 2
            screen.blit(font.render(f"{int(weight)}", True, GREEN), (mid_x, mid_y))
    for idx, (x, y) in enumerate(nodes):
        pygame.draw.circle(screen, BLUE, (x, y), 10)
        screen.blit(font.render(str(idx), True, BLACK), (x + 15, y - 10))

def main():
    global current_mst, parent_structure, algorithm_started, mst_completed, show_union_find, step_completed, current_u, current_v
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not algorithm_started:
                    algorithm_started = True
                if mst_completed and event.key == pygame.K_RETURN:
                    show_union_find = True
                if not mst_completed and event.key == pygame.K_RETURN and not step_completed:
                    step_completed = True
                if step_completed:
                    step_completed = False  # Move para o próximo passo

        if algorithm_started and not mst_completed:
            try:
                current_mst, parent_structure, current_u, current_v = next(generator)
            except StopIteration:
                mst_completed = True
        draw_graph(highlight_edge=(current_u, current_v) if not mst_completed else None)
        pygame.display.flip()
        clock.tick(2)  # Controla a velocidade da animação
    pygame.quit()

if __name__ == "__main__":
    main()
