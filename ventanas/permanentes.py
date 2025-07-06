import pygame
import os

import codigo.constantes as constantes

ventana = pygame.display.set_mode((constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA))

def solicitar_nombre(pantalla, fuente):
    nombre = ""
    ingresando_nombre = True
    
    while ingresando_nombre:
        pantalla.fill(constantes.NEGRO)  # Limpiar la pantalla
        
        # Mostrar el mensaje de ingresar el nombre
        mensaje_nombre = fuente.render("Ingrese su nombre:", True, constantes.BLANCO)
        rect_mensaje_nombre = mensaje_nombre.get_rect(center=(pantalla.get_width() // 2, pantalla.get_height() // 2 - 20))
        pantalla.blit(mensaje_nombre, rect_mensaje_nombre)
        
        # Mostrar el nombre que se está ingresando
        mensaje_nombre_actual = fuente.render(nombre, True, constantes.BLANCO)
        rect_mensaje_nombre_actual = mensaje_nombre_actual.get_rect(center=(pantalla.get_width() // 2, pantalla.get_height() // 2 + 20))
        pantalla.blit(mensaje_nombre_actual, rect_mensaje_nombre_actual)
        
        pygame.display.update()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    ingresando_nombre = False
                elif evento.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]
                else:
                    nombre += evento.unicode
                    
    return nombre

def guardar_puntaje(nombre_jugador, puntaje, nivel_alcanzado):
    directorio_puntajes = "assets"
    archivo_puntajes = os.path.join(directorio_puntajes, "puntajes.txt")

    if not os.path.exists(archivo_puntajes):
        with open(archivo_puntajes, "w") as archivo:
            archivo.write("Nombre,Puntaje,Nivel\n")  # Escribir encabezado

    with open(archivo_puntajes, "a") as archivo:
        archivo.write(f"{nombre_jugador},{puntaje},{nivel_alcanzado}\n")

def leer_puntajes():
    puntajes = []
    try:
        with open("assets/puntajes.txt", "r") as file:
            for line in file.readlines()[1:]:  # Omitir encabezado
                nombre, puntaje, nivel = line.strip().split(",")
                puntajes.append((nombre, int(puntaje), int(nivel)))
    except FileNotFoundError:
        pass
    return puntajes

def borrar_puntajes():
    with open("assets/puntajes.txt", "w") as file:
        file.write("Nombre,Puntaje,Nivel\n")  # Escribir encabezado vacío
