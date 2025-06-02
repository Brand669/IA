import pygame
import random
import numpy as np
import csv
import os
from sklearn.neighbors import KNeighborsClassifier

# Inicializar Pygame
pygame.init()

# Modelo KNN
modelo_knn = KNeighborsClassifier(n_neighbors=3)

# Función para entrenar el modelo
def entrenar_modelo():
    global modelo_knn, datos_modelo
    if len(datos_modelo) > 0:
        X = np.array([list(caracteristicas) for caracteristicas, accion in datos_modelo])
        y = np.array([accion for _, accion in datos_modelo])
        modelo_knn.fit(X, y)
        print("Modelo KNN entrenado con los datos:", datos_modelo)
    else:
        print("No hay datos suficientes para entrenar el modelo.")

# Función para predecir la acción en modo automático
def predecir_accion():
    global jugador, bala, bala_vertical, salto, en_suelo
    distancia_horizontal = abs(jugador.x - bala.x)
    distancia_vertical = abs(jugador.x - bala_vertical.x) if bala_vertical.y < h else 999

    if distancia_horizontal < 100 and en_suelo:
        salto = True
        en_suelo = False
        return

    if distancia_vertical < 30 and bala_vertical.y < jugador.y:
        jugador.x += 5
        if jugador.x > w - jugador.width:
            jugador.x = w - jugador.width
        return

    if jugador.x > 0:
        jugador.x -= 2
        if jugador.x < 0:
            jugador.x = 0

# Dimensiones
tamano = (800, 400)
w, h = tamano
pantalla = pygame.display.set_mode(tamano)
pygame.display.set_caption("Juego: KNN - Movimiento del Jugador")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Variables
salto = False
salto_altura = 15
gravedad = 1
en_suelo = True
pausa = False
fuente = pygame.font.SysFont('Arial', 24)
menu_activo = True
modo_auto = False
urlInicial = 'C:/Users/Brandon/Desktop/ITM/IA/DecisionTree/'
datos_modelo = []

# Imágenes
jugador_frames = [
    pygame.image.load(urlInicial + 'assets/sprites/mono_frame_1.png'),
    pygame.image.load(urlInicial + 'assets/sprites/mono_frame_2.png'),
    pygame.image.load(urlInicial + 'assets/sprites/mono_frame_3.png'),
    pygame.image.load(urlInicial + 'assets/sprites/mono_frame_4.png')
]
bala_img = pygame.image.load(urlInicial + 'assets/sprites/purple_ball.png')
fondo_img = pygame.image.load(urlInicial + 'assets/game/fondo2.png')
nave_img = pygame.image.load(urlInicial + 'assets/game/ufo.png')
menu_img = pygame.image.load(urlInicial + 'assets/game/menu.png')
fondo_img = pygame.transform.scale(fondo_img, tamano)

# Objetos
jugador = pygame.Rect(0, h - 100, 32, 48)
bala = pygame.Rect(w - 50, h - 90, 16, 16)
bala_vertical = pygame.Rect(5, 0, 16, 16)
nave = pygame.Rect(w - 100, h - 100, 64, 64)

# Animación
current_frame = 0
frame_speed = 10
frame_count = 0

# Velocidades
velocidad_bala = -10
velocidad_bala_vertical = 7
bala_disparada = False

# Fondo
fondo_x1 = 0
fondo_x2 = w

def disparar_bala():
    global bala_disparada, velocidad_bala
    if not bala_disparada:
        velocidad_bala = random.randint(-15, -8)
        bala_disparada = True

def reset_bala():
    global bala, bala_disparada
    bala.x = w - 50
    bala_disparada = False

def reset_bala_vertical():
    global bala_vertical
    bala_vertical.y = 0
    bala_vertical.x = 5

def manejar_salto():
    global jugador, salto, salto_altura, gravedad, en_suelo
    if salto:
        jugador.y -= salto_altura
        salto_altura -= gravedad
        if jugador.y >= h - 100:
            jugador.y = h - 100
            salto = False
            salto_altura = 15
            en_suelo = True

def update():
    global bala, velocidad_bala, current_frame, frame_count, fondo_x1, fondo_x2, bala_vertical
    fondo_x1 -= 1
    fondo_x2 -= 1
    if fondo_x1 <= -w: fondo_x1 = w
    if fondo_x2 <= -w: fondo_x2 = w
    pantalla.blit(fondo_img, (fondo_x1, 0))
    pantalla.blit(fondo_img, (fondo_x2, 0))
    frame_count += 1
    if frame_count >= frame_speed:
        current_frame = (current_frame + 1) % len(jugador_frames)
        frame_count = 0
    pantalla.blit(jugador_frames[current_frame], (jugador.x, jugador.y))
    pantalla.blit(nave_img, (nave.x, nave.y))

    if bala_disparada:
        bala.x += velocidad_bala
        if bala.x < 0:
            reset_bala()
    pantalla.blit(bala_img, (bala.x, bala.y))

    bala_vertical.y += velocidad_bala_vertical
    if bala_vertical.y > h:
        reset_bala_vertical()
    pantalla.blit(bala_img, (bala_vertical.x, bala_vertical.y))

    if jugador.colliderect(bala) or jugador.colliderect(bala_vertical):
        print("Colisión detectada!")
        reiniciar_juego()

# Almacena datos como (features, action) => ((v_bala, d_horizontal, d_vertical), acción)
datos_modelo = []

def guardar_datos():
    global jugador, bala, bala_vertical, velocidad_bala
    distancia_horizontal = abs(jugador.x - bala.x)
    distancia_vertical = abs(jugador.x - bala_vertical.x) if bala_vertical.y < h else 999
    accion = 0
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and en_suelo:
        accion = 1  # salto
    elif keys[pygame.K_a]:
        accion = 2  # izquierda
    elif keys[pygame.K_d]:
        accion = 3  # derecha
    datos_modelo.append(((velocidad_bala, distancia_horizontal, distancia_vertical), accion))


def entrenar_modelo():
    if len(datos_modelo) > 0:
        X = [list(features) for features, _ in datos_modelo]
        y = [accion for _, accion in datos_modelo]
        modelo_knn.fit(X, y)
        print("Modelo entrenado con", len(X), "datos.")
    else:
        print("No hay datos para entrenar.")

def predecir_accion():
    global jugador, bala, bala_vertical, salto, en_suelo
    distancia_horizontal = abs(jugador.x - bala.x)
    distancia_vertical = abs(jugador.x - bala_vertical.x) if bala_vertical.y < h else 999
    entrada = np.array([[velocidad_bala, distancia_horizontal, distancia_vertical]])

    if len(datos_modelo) > 0:
        accion = modelo_knn.predict(entrada)[0]

        if accion == 1 and en_suelo:
            salto = True
            en_suelo = False
        elif accion == 2:
            jugador.x -= 5
            if jugador.x < 0:
                jugador.x = 0
        elif accion == 3:
            jugador.x += 5
            if jugador.x > w - jugador.width:
                jugador.x = w - jugador.width
        # Acción 0 = quedarse quieto (o volver tranquilo a x = 0)
        elif accion == 0:
            if jugador.x > 0:
                jugador.x -= 2
                if jugador.x < 0:
                    jugador.x = 0


def guardar_en_csv(nombre_archivo="datos_movimiento.csv"):
    with open(nombre_archivo, mode='w', newline='') as archivo:
        writer = csv.writer(archivo)
        writer.writerow(["velocidad_bala", "distancia_horizontal", "distancia_vertical", "accion"])
        for (features, accion) in datos_modelo:
            writer.writerow(list(features) + [accion])
    print(f"Datos guardados en {nombre_archivo}")

def borrar_datos(nombre_archivo="datos_movimiento.csv"):
    global datos_modelo
    datos_modelo.clear()
    if os.path.exists(nombre_archivo):
        os.remove(nombre_archivo)
        print(f"Datos borrados y archivo eliminado: {nombre_archivo}")
    else:
        print("Datos borrados. No había archivo en disco.")

def pausa_juego():
    global pausa
    pausa = not pausa
    if pausa:
        print("Juego pausado. Datos registrados:", datos_modelo)
    else:
        print("Juego reanudado.")

def mostrar_menu():
    global menu_activo, modo_auto
    pantalla.fill(NEGRO)
    texto = fuente.render("Presiona 'A' para Auto (KNN), 'M' para Manual, o 'Q' para Salir", True, BLANCO)
    pantalla.blit(texto, (w // 4, h // 2))
    pygame.display.flip()
    while menu_activo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_a:
                    modo_auto = True
                    entrenar_modelo()
                    menu_activo = False
                elif evento.key == pygame.K_m:
                    modo_auto = False
                    menu_activo = False
                elif evento.key == pygame.K_q:
                    guardar_en_csv()
                    pygame.quit()
                    exit()

def reiniciar_juego():
    global menu_activo, jugador, bala, nave, bala_disparada, salto, en_suelo, bala_vertical
    menu_activo = True
    jugador.x, jugador.y = 0, h - 100
    reset_bala()
    reset_bala_vertical()
    nave.x, nave.y = w - 100, h - 100
    bala_disparada = False
    salto = False
    en_suelo = True
    mostrar_menu()

def main():
    global salto, en_suelo, bala_disparada
    reloj = pygame.time.Clock()
    mostrar_menu()
    correr = True
    while correr:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                correr = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and en_suelo and not pausa and not modo_auto:
                    salto = True
                    en_suelo = False
                if evento.key == pygame.K_p:
                    pausa_juego()
                if evento.key == pygame.K_q:
                    guardar_en_csv()
                    pygame.quit()
                    exit()
                if evento.key == pygame.K_r:
                    borrar_datos()
        if not pausa:
            keys = pygame.key.get_pressed()
            if not modo_auto:
                if keys[pygame.K_a]:
                    jugador.x -= 5
                    if jugador.x < 0:
                        jugador.x = 0
                if keys[pygame.K_d]:
                    jugador.x += 5
                    if jugador.x > w - jugador.width:
                        jugador.x = w - jugador.width
                if keys[pygame.K_w] and en_suelo:
                    salto = True
                    en_suelo = False
                if salto:
                    manejar_salto()
                guardar_datos()
            else:
                predecir_accion()
                manejar_salto()
            if not bala_disparada:
                disparar_bala()
            update()
        pygame.display.flip()
        reloj.tick(30)
    pygame.quit()

if __name__ == "__main__":
    main()
