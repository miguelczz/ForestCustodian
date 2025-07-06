import pygame
import sys

import codigo.constantes as constantes

# Función para dibujar texto con sombra
def dibujar_texto_con_sombra(ventana, texto, font, color, x, y, offset_x, offset_y):
    sombra_color = (0, 0, 0)  # Color de la sombra (negro)
    texto_surface = font.render(texto, True, color)
    sombra_surface = font.render(texto, True, sombra_color)
    ventana.blit(sombra_surface, (x + offset_x, y + offset_y))  # Dibuja la sombra desplazada
    ventana.blit(texto_surface, (x, y))  # Dibuja el texto principal
    
    # Función para mostrar los puntajes
def mostrar_puntajes(fuente):
    # Inicializar Pygame
    pygame.init()

    ventana_puntajes = pygame.display.set_mode((constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA))
    pygame.display.set_caption("Puntajes")

    # Leer puntajes desde el archivo
    try:
        with open("assets/puntajes.txt", "r") as f:
            puntajes = [line.strip().split(",") for line in f.readlines()[1:] if "," in line]
    except FileNotFoundError:
        puntajes = []

    run_puntajes = True
    while run_puntajes:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if boton_borrar.collidepoint(event.pos):
                    with open("assets/puntajes.txt", "w") as f:
                        f.write("Nombre,Puntaje,Nivel\n")  # Escribir encabezado vacío
                    puntajes = []  # Vaciar la lista de puntajes
                if boton_inicio.collidepoint(event.pos):
                    # ventana_inicio(ventana)
                    run_puntajes = False

        ventana_puntajes.fill(constantes.NEGRO)

        # Dibujar los puntajes en la ventana
        for i, (nombre, puntaje, nivel) in enumerate(puntajes):
            text_surface = fuente.render(f"{nombre}: {puntaje} puntos, Nivel {nivel}", True, constantes.BLANCO)
            ventana_puntajes.blit(text_surface, (50, 50 + i * 30))

        # Dibujar el botón de borrar puntajes
        boton_borrar = pygame.Rect(640, 520, 233, 50)
        pygame.draw.rect(ventana_puntajes, constantes.ROJO, boton_borrar)
        texto_borrar = fuente.render("Borrar Puntajes", True, constantes.BLANCO)
        ventana_puntajes.blit(texto_borrar, (655, 530))
        
        # Botón para volver al inicio
        boton_inicio = pygame.Rect(410, 520, 200, 50) # Modificar tamaño y posicion de botones
        pygame.draw.rect(ventana_puntajes, constantes.AZUL, boton_inicio)
        inicio_texto = fuente.render("Inicio", True, constantes.BLANCO)
        ventana_puntajes.blit(inicio_texto, (470, 530)) # Posicion del texto

        pygame.display.flip()  # Actualizar la pantalla

# Función para la ventana de inicio
def ventana_inicio(ventana):
    fondo = pygame.image.load("assets/images/start_items/forest_inicio.jpg")
    fondo = pygame.transform.scale(fondo, (ventana.get_width(), ventana.get_height()))
    titulo_font = pygame.font.Font("assets/fonts/mago3.ttf", 110)
    boton_font = pygame.font.Font("assets/fonts/mago3.ttf", 36)  # Fuente para los botones

    titulo_texto = "Forest Custodian"
    boton_texto = "Jugar"
    boton_texto_puntajes = "Puntajes"

    # Tamaño y posición de los botones
    tamaño_normal = (190, 50)
    tamaño_escalado = (210, 65)
    
    boton_jugar = pygame.Rect((ventana.get_width() - tamaño_normal[0]) // 2 - 110, (ventana.get_height() - tamaño_normal[1]) // 2 + 150, *tamaño_normal)
    boton_puntaje = pygame.Rect((ventana.get_width() - tamaño_normal[0]) // 2 + 110, (ventana.get_height() - tamaño_normal[1]) // 2 + 150, *tamaño_normal)
    
    # Música
    pygame.mixer.music.load("assets/sounds/music/Three Red Hearts - Penguin Town.ogg")
    pygame.mixer.music.play(-1)

    run = True
    while run:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                elif evento.key == pygame.K_UP:
                    constantes.VOLUMEN = min(1.0, constantes.VOLUMEN + 0.1)
                    pygame.mixer.music.set_volume(constantes.VOLUMEN)
                elif evento.key == pygame.K_DOWN:
                    constantes.VOLUMEN = max(0.0, constantes.VOLUMEN - 0.1)
                    pygame.mixer.music.set_volume(constantes.VOLUMEN)
                elif evento.key == pygame.K_SPACE:
                    pygame.mixer.music.stop()
                    return
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_jugar.collidepoint(evento.pos):
                    pygame.mixer.music.stop()
                    return
                elif boton_puntaje.collidepoint(evento.pos):
                    mostrar_puntajes(boton_font)  # Pasar la fuente correcta

        cursor_sobre_boton_jugar = boton_jugar.collidepoint(pygame.mouse.get_pos())
        cursor_sobre_boton_puntaje = boton_puntaje.collidepoint(pygame.mouse.get_pos())

        if cursor_sobre_boton_jugar:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            boton_jugar.inflate_ip((tamaño_escalado[0] - boton_jugar.width) // 10, (tamaño_escalado[1] - boton_jugar.height) // 10)
        else:
            boton_jugar.inflate_ip((tamaño_normal[0] - boton_jugar.width) // 10, (tamaño_normal[1] - boton_jugar.height) // 10)
        
        if cursor_sobre_boton_puntaje:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            boton_puntaje.inflate_ip((tamaño_escalado[0] - boton_puntaje.width) // 10, (tamaño_escalado[1] - boton_puntaje.height) // 10)
        else:
            boton_puntaje.inflate_ip((tamaño_normal[0] - boton_puntaje.width) // 10, (tamaño_normal[1] - boton_puntaje.height) // 10)

        ventana.blit(fondo, (0, 0))

        # Dibuja el texto con sombra
        dibujar_texto_con_sombra(ventana, titulo_texto, titulo_font, (255, 255, 255), 115, 150, 4, 2)

        # Dibuja los botones
        pygame.draw.rect(ventana, (85, 107, 47), boton_jugar)
        pygame.draw.rect(ventana, (0, 0, 0), boton_jugar, 3)
        texto_boton = boton_font.render(boton_texto, True, (255, 255, 255))
        ventana.blit(texto_boton, (boton_jugar.x + (boton_jugar.width - texto_boton.get_width()) // 2, boton_jugar.y + (boton_jugar.height - texto_boton.get_height()) // 2))

        pygame.draw.rect(ventana, (85, 107, 47), boton_puntaje)
        pygame.draw.rect(ventana, (0, 0, 0), boton_puntaje, 3) # Borde
        texto_boton_puntajes = boton_font.render(boton_texto_puntajes, True, (255, 255, 255))
        ventana.blit(texto_boton_puntajes, (boton_puntaje.x + (boton_puntaje.width - texto_boton_puntajes.get_width()) // 2, boton_puntaje.y + (boton_puntaje.height - texto_boton_puntajes.get_height()) // 2))

        pygame.display.update()

    return True

# Inicialización de Pygame y configuración de la ventana
pygame.init()
ventana = pygame.display.set_mode((900, 600))
pygame.display.set_caption("Forest Custodian")

# Llamada a la función de inicio de ventana
ventana_inicio(ventana)
