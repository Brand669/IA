import pygame
from queue import PriorityQueue

# Configuraciones iniciales
ANCHO_VENTANA = 800
VENTANA = pygame.display.set_mode((ANCHO_VENTANA, ANCHO_VENTANA))
pygame.display.set_caption("Visualización de Nodos - A*")

# Colores (RGB)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (128, 128, 128)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
NARANJA = (255, 165, 0)
PURPURA = (128, 0, 128)

class Nodo:
    def __init__(self, fila, col, ancho, total_filas):
        self.fila = fila
        self.col = col
        self.x = fila * ancho
        self.y = col * ancho
        self.color = BLANCO
        self.ancho = ancho
        self.total_filas = total_filas
        self.vecinos = []
    
    def get_pos(self):
        return self.fila, self.col

    def es_pared(self):
        return self.color == NEGRO

    def hacer_pared(self):
        self.color = NEGRO
    
    def hacer_inicio(self):
        self.color = NARANJA
    
    def hacer_fin(self):
        self.color = VERDE
    
    def hacer_cerrado(self):
        self.color = ROJO
    
    def hacer_abierto(self):
        self.color = PURPURA
    
    def hacer_camino(self):
        self.color = VERDE
    
    def dibujar(self, ventana):
        pygame.draw.rect(ventana, self.color, (self.x, self.y, self.ancho, self.ancho))

    def actualizar_vecinos(self, grid):
        self.vecinos = []
        direcciones = [
            (1, 0), (-1, 0), (0, 1), (0, -1),
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]
        for df, dc in direcciones:
            nf, nc = self.fila + df, self.col + dc
            if 0 <= nf < self.total_filas and 0 <= nc < self.total_filas:
                if not grid[nf][nc].es_pared():
                    self.vecinos.append(grid[nf][nc])

def dibujar(ventana, grid, filas, ancho):
    ventana.fill(BLANCO)
    for fila in grid:
        for nodo in fila:
            nodo.dibujar(ventana)
    pygame.display.update()

def heuristica(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def algoritmo_a_star(grid, inicio, fin):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, inicio))
    came_from = {}
    g_score = {nodo: float("inf") for fila in grid for nodo in fila}
    g_score[inicio] = 0
    f_score = {nodo: float("inf") for fila in grid for nodo in fila}
    f_score[inicio] = heuristica(inicio.get_pos(), fin.get_pos())
    open_set_hash = {inicio}
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        actual = open_set.get()[2]
        open_set_hash.remove(actual)
        if actual == fin:
            while actual in came_from:
                actual = came_from[actual]
                actual.hacer_camino()
                dibujar(VENTANA, grid, len(grid), ANCHO_VENTANA)
            return True
        for vecino in actual.vecinos:
            temp_g_score = g_score[actual] + 1
            if temp_g_score < g_score[vecino]:
                came_from[vecino] = actual
                g_score[vecino] = temp_g_score
                f_score[vecino] = temp_g_score + heuristica(vecino.get_pos(), fin.get_pos())
                if vecino not in open_set_hash:
                    count += 1
                    open_set.put((f_score[vecino], count, vecino))
                    open_set_hash.add(vecino)
                    vecino.hacer_abierto()
        dibujar(VENTANA, grid, len(grid), ANCHO_VENTANA)
        if actual != inicio:
            actual.hacer_cerrado()
    return False

def main():
    FILAS = 20
    grid = [[Nodo(i, j, ANCHO_VENTANA // FILAS, FILAS) for j in range(FILAS)] for i in range(FILAS)]
    inicio, fin = None, None
    corriendo = True
    while corriendo:
        dibujar(VENTANA, grid, FILAS, ANCHO_VENTANA)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo = False
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                fila, col = pos[1] // (ANCHO_VENTANA // FILAS), pos[0] // (ANCHO_VENTANA // FILAS)
                nodo = grid[fila][col]
                if not inicio:
                    inicio = nodo
                    inicio.hacer_inicio()
                elif not fin and nodo != inicio:
                    fin = nodo
                    fin.hacer_fin()
                elif nodo != inicio and nodo != fin:
                    nodo.hacer_pared()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and inicio and fin:
                    for fila in grid:
                        for nodo in fila:
                            nodo.actualizar_vecinos(grid)
                    algoritmo_a_star(grid, inicio, fin)
    pygame.quit()

main()