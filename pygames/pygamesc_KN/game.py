import pygame
import random
import numpy as np
from sklearn.neighbors import KNeighborsClassifier

pygame.init()

# --- Variables globales y constantes ---
w, h = 800, 400
pantalla = pygame.display.set_mode((w, h))
pygame.display.set_caption("Mono con KNN")

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

jugador = pygame.Rect(50, h - 100, 32, 48)
bala = pygame.Rect(w - 50, h - 90, 16, 16)
bala_vertical = pygame.Rect(60, 0, 16, 16)

vel_bala = -10
vel_bala_vertical = 7
bala_disparada = False

salto = False
salto_altura = 15
gravedad = 1
en_suelo = True

font = pygame.font.SysFont('Arial', 24)

# Datos para entrenar
datos_modelo = []
modelo = KNeighborsClassifier(n_neighbors=5)

modo_auto = False
pausa = False
game_over = False

# --- Funciones ---
def reiniciar_juego():
    global jugador, bala, bala_vertical, salto, en_suelo, bala_disparada, game_over
    jugador.x, jugador.y = 50, h - 100
    bala.x, bala.y = w - 50, h - 90
    bala_vertical.x, bala_vertical.y = 60, 0
    salto = False
    en_suelo = True
    bala_disparada = False
    game_over = False

def disparar_bala():
    global bala_disparada, vel_bala
    if not bala_disparada:
        vel_bala = random.randint(-15, -8)
        bala_disparada = True

def reset_bala():
    global bala, bala_disparada
    bala.x = w - 50
    bala_disparada = False

def reset_bala_vertical():
    global bala_vertical
    bala_vertical.y = 0

def manejar_salto():
    global jugador, salto, salto_altura, en_suelo
    if salto:
        jugador.y -= salto_altura
        salto_altura -= gravedad
        if jugador.y >= h - 100:
            jugador.y = h - 100
            salto = False
            reiniciar_salto()

def reiniciar_salto():
    global salto_altura, en_suelo
    salto_altura = 15
    en_suelo = True

def generar_datos_sinteticos():
    global datos_modelo
    for vel in range(-15, -7):  # velocidad bala horizontal
        for dist_h in range(0, w + 1, 40):  # distancia horizontal
            for dist_v in range(0, h + 1, 40):  # distancia vertical
                accion = 0
                # Si bala horizontal cerca y en suelo => saltar
                if dist_h < 100 and vel < -8:
                    accion = 1
                # Si bala vertical cerca => mover izquierda o derecha aleatorio
                elif dist_v < 120:
                    accion = random.choice([2, 3])
                else:
                    accion = 0
                # Añadimos posición fija del jugador (50, h-100) para consistencia
                datos_modelo.append(((vel, dist_h, dist_v, 50, h - 100), accion))

def entrenar_modelo():
    global modelo, datos_modelo
    if len(datos_modelo) > 0:
        X = np.array([list(x) for x, y in datos_modelo])
        y = np.array([y for x, y in datos_modelo])
        modelo.fit(X, y)
        print("Modelo entrenado con", len(datos_modelo), "datos.")
    else:
        print("No hay datos para entrenar.")

def predecir_accion():
    dist_hor = abs(jugador.x - bala.x)
    dist_vert = abs(jugador.x - bala_vertical.x) if bala_vertical.y < h else 999
    entrada = np.array([[vel_bala, dist_hor, dist_vert, jugador.x, jugador.y]])
    try:
        return modelo.predict(entrada)[0]
    except:
        return 0  # Si no está entrenado aún

def update():
    global bala, bala_vertical, bala_disparada
    pantalla.fill(NEGRO)

    # Actualizar bala horizontal
    if bala_disparada:
        bala.x += vel_bala
        if bala.x < 0:
            reset_bala()

    # Actualizar bala vertical
    bala_vertical.y += vel_bala_vertical
    if bala_vertical.y > h:
        reset_bala_vertical()

    # Dibujar elementos
    pygame.draw.rect(pantalla, (0, 255, 0), jugador)
    pygame.draw.rect(pantalla, (255, 0, 0), bala)
    pygame.draw.rect(pantalla, (255, 0, 255), bala_vertical)

    # Detectar colisiones
    if jugador.colliderect(bala) or jugador.colliderect(bala_vertical):
        return True
    return False

def mostrar_menu():
    global modo_auto
    pantalla.fill(NEGRO)
    texto = font.render("Presiona 'A' para AUTO, 'M' para MANUAL, 'Q' para salir", True, BLANCO)
    pantalla.blit(texto, (w // 6, h // 2))
    pygame.display.flip()
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_a:
                    modo_auto = True
                    generar_datos_sinteticos()
                    entrenar_modelo()
                    return
                elif evento.key == pygame.K_m:
                    modo_auto = False
                    datos_modelo.clear()
                    return
                elif evento.key == pygame.K_q:
                    pygame.quit()
                    exit()

def guardar_datos(accion):
    dist_hor = abs(jugador.x - bala.x)
    dist_vert = abs(jugador.x - bala_vertical.x) if bala_vertical.y < h else 999
    datos_modelo.append(((vel_bala, dist_hor, dist_vert, jugador.x, jugador.y), accion))

def main():
    global salto, en_suelo, pausa, bala_disparada, game_over
    reloj = pygame.time.Clock()

    while True:
        mostrar_menu()
        reiniciar_juego()
        game_over = False
        pausa = False

        while not game_over:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE and en_suelo and not pausa and not modo_auto:
                        salto = True
                        en_suelo = False
                    if evento.key == pygame.K_p:
                        pausa = not pausa
                    if evento.key == pygame.K_q:
                        pygame.quit()
                        exit()

            if not pausa:
                if modo_auto:
                    accion = predecir_accion()
                    # Accion: 0=ninguna, 1=salto, 2=mover izquierda, 3=mover derecha
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
                else:
                    keys = pygame.key.get_pressed()
                    accion = 0
                    if keys[pygame.K_w] and en_suelo:
                        salto = True
                        en_suelo = False
                        accion = 1
                    elif keys[pygame.K_a]:
                        jugador.x -= 5
                        if jugador.x < 0:
                            jugador.x = 0
                        accion = 2
                    elif keys[pygame.K_d]:
                        jugador.x += 5
                        if jugador.x > w - jugador.width:
                            jugador.x = w - jugador.width
                        accion = 3

                    guardar_datos(accion)

                if salto:
                    manejar_salto()

                if not bala_disparada:
                    disparar_bala()

                colision = update()
                if colision:
                    print("Has muerto!")
                    game_over = True

            pygame.display.flip()
            reloj.tick(30)

if __name__ == "__main__":
    main()
