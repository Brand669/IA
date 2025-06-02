import pygame
from queue import PriorityQueue

# Configuraciones iniciales
ANCHO_VENTANA = 800
VENTANA = pygame.display.set_mode((ANCHO_VENTANA, ANCHO_VENTANA))
pygame.display.set_caption("Visualización de Nodos")

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
        self.g = float("inf")  # Coste desde el inicio
        self.f = float("inf")  # g + h
        self.h = 0  # Heurística

    def __lt__(self, otro):
        return self.f < otro.f  # Compara nodos usando f-score

    def actualizar_vecinos(self, grid):
        """Determina los vecinos accesibles (no paredes), incluyendo diagonales"""
        self.vecinos = []
        direcciones = [
            (-1, 0), (1, 0), (0, -1), (0, 1),       # Arriba, Abajo, Izquierda, Derecha
            (-1, -1), (-1, 1), (1, -1), (1, 1)      # Diagonales
        ]
        for dx, dy in direcciones:
            nueva_fila = self.fila + dx
            nueva_col = self.col + dy
            if 0 <= nueva_fila < self.total_filas and 0 <= nueva_col < self.total_filas:
                vecino = grid[nueva_fila][nueva_col]
                if not vecino.es_pared():
                    self.vecinos.append(vecino)


    def get_pos(self):
        return self.fila, self.col

    def es_pared(self):
        return self.color == NEGRO

    def es_inicio(self):
        return self.color == NARANJA

    def es_fin(self):
        return self.color == PURPURA

    def restablecer(self):
        self.color = BLANCO

    def hacer_inicio(self):
        self.color = NARANJA

    def hacer_pared(self):
        self.color = NEGRO

    def hacer_fin(self):
        self.color = PURPURA

    def dibujar(self, ventana):
        pygame.draw.rect(ventana, self.color, (self.x, self.y, self.ancho, self.ancho))

    

def heuristica(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def a_star(dibujar, grid, inicio, objetivo):
    open_set = PriorityQueue()
    open_set.put((0, inicio))
    came_from = {}
    g_score = {nodo: float("inf") for fila in grid for nodo in fila}
    f_score = {nodo: float("inf") for fila in grid for nodo in fila}

    g_score[inicio] = 0
    f_score[inicio] = heuristica(inicio.get_pos(), objetivo.get_pos())

    open_set_hash = {inicio}

    while not open_set.empty():
        current = open_set.get()[1]
        open_set_hash.remove(current)

        if current == objetivo:
            reconstruir_camino(came_from, current, dibujar)
            return True

        for vecino in current.vecinos:
            # Detectar si es un movimiento diagonal
            dx = abs(current.fila - vecino.fila)
            dy = abs(current.col - vecino.col)
            costo = 1.4 if dx == 1 and dy == 1 else 1  # Diagonal = 1.4, Ortogonal = 1.0

            tentative_g_score = g_score[current] + costo

            if tentative_g_score < g_score[vecino]:
                came_from[vecino] = current
                g_score[vecino] = tentative_g_score
                f_score[vecino] = g_score[vecino] + heuristica(vecino.get_pos(), objetivo.get_pos())

                if vecino not in open_set_hash:
                    open_set.put((f_score[vecino], vecino))
                    open_set_hash.add(vecino)
                    if not vecino.es_inicio() and not vecino.es_fin():
                        vecino.color = GRIS  # Marca el vecino como visitado

        dibujar()

        if current != inicio and current != objetivo:
            current.color = ROJO  # Marca el nodo como procesado

    return False


def reconstruir_camino(came_from, current, dibujar):
    while current in came_from:
        current = came_from[current]
        if not current.es_inicio() and not current.es_fin():
            current.color = VERDE  # Marca el camino óptimo
        dibujar()

def crear_grid(filas, ancho):
    grid = []
    ancho_nodo = ancho // filas
    for i in range(filas):
        grid.append([])
        for j in range(filas):
            nodo = Nodo(i, j, ancho_nodo, filas)
            grid[i].append(nodo)
    return grid

def dibujar_grid(ventana, filas, ancho):
    ancho_nodo = ancho // filas
    for i in range(filas):
        pygame.draw.line(ventana, GRIS, (0, i * ancho_nodo), (ancho, i * ancho_nodo))
        for j in range(filas):
            pygame.draw.line(ventana, GRIS, (j * ancho_nodo, 0), (j * ancho_nodo, ancho))

def dibujar(ventana, grid, filas, ancho):
    ventana.fill(BLANCO)
    for fila in grid:
        for nodo in fila:
            nodo.dibujar(ventana)

    dibujar_grid(ventana, filas, ancho)
    pygame.display.update()

def obtener_click_pos(pos, filas, ancho):
    ancho_nodo = ancho // filas
    y, x = pos
    fila = y // ancho_nodo
    col = x // ancho_nodo
    return fila, col

def main(ventana, ancho):
    FILAS = 11
    grid = crear_grid(FILAS, ancho)

    inicio = None
    fin = None

    corriendo = True

    while corriendo:
        dibujar(ventana, grid, FILAS, ancho)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and inicio and fin:
                # Actualizar vecinos antes de ejecutar A*
                    for fila in grid:
                        for nodo in fila:
                            nodo.actualizar_vecinos(grid)

                    a_star(lambda: dibujar(VENTANA, grid, FILAS, ANCHO_VENTANA), grid, inicio, fin)


            if pygame.mouse.get_pressed()[0]:  # Click izquierdo
                pos = pygame.mouse.get_pos()
                fila, col = obtener_click_pos(pos, FILAS, ancho)
                nodo = grid[fila][col]
                if not inicio and nodo != fin:
                    inicio = nodo
                    inicio.hacer_inicio()

                elif not fin and nodo != inicio:
                    fin = nodo
                    fin.hacer_fin()

                elif nodo != fin and nodo != inicio:
                    nodo.hacer_pared()

            elif pygame.mouse.get_pressed()[2]:  # Click derecho
                pos = pygame.mouse.get_pos()
                fila, col = obtener_click_pos(pos, FILAS, ancho)
                nodo = grid[fila][col]
                nodo.restablecer()
                if nodo == inicio:
                    inicio = None
                elif nodo == fin:
                    fin = None

    pygame.quit()

main(VENTANA, ANCHO_VENTANA)