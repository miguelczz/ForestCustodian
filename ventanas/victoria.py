import pygame

import codigo.constantes as constantes
from ventanas.inicio import ventana_inicio

def mostrar_victoria(ventana):
    
    fuente = pygame.font.Font("assets/fonts/mago3.ttf", 60)
    
    # Texto Game Over y obtencion del rectangula para posicionarlo   
    game_over_texto = fuente.render("Has ganado el nivel!", True, constantes.DORADO)
    game_over_rect = game_over_texto.get_rect(center=(constantes.ANCHO_VENTANA // 2, constantes.ALTO_VENTANA // 2 - 100))
    
    game_over_ventana = pygame.Surface((constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA))
    game_over_ventana.fill(constantes.NEGRO)
    game_over_ventana.blit(game_over_texto, game_over_rect)
    ventana.blit(game_over_ventana, (0, 0))
    
    pygame.display.update()

def botones_victoria(ventana, font, jugador):
    
    # Botón para reiniciar nivel
    boton_reiniciar = pygame.Rect(100, 430, 200, 50) # Modificar tamaño y posicion de botones
    pygame.draw.rect(ventana, constantes.VERDE, boton_reiniciar)
    reiniciar_texto = font.render("Reiniciar Nivel", True, constantes.BLANCO)
    ventana.blit(reiniciar_texto, (120, 440)) # Posicion del texto
    
    # Botón para volver al inicio
    boton_inicio = pygame.Rect(600, 430, 200, 50) # Modificar tamaño y posicion de botones
    pygame.draw.rect(ventana, constantes.AZUL, boton_inicio)
    inicio_texto = font.render("Inicio", True, constantes.BLANCO)
    ventana.blit(inicio_texto, (670, 440)) # Posicion del texto
    
    # Botón para continuar en el juego
    boton_continuar = pygame.Rect(350, 430, 200, 50) # Modificar tamaño y posicion de botones
    pygame.draw.rect(ventana, constantes.NARANJA, boton_continuar)
    inicio_texto = font.render("Continuar", True, constantes.BLANCO)
    ventana.blit(inicio_texto, (400, 440)) # Posicion del texto
    
    pygame.display.update()

    # Bucle para esperar la respuesta del usuario
    while True:
        # Se hace llamado iterativo para dar funcionalidad a los botones
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton_reiniciar.collidepoint(event.pos):
                    reiniciar_nivel(jugador)
                    return "reiniciar"
                elif boton_inicio.collidepoint(event.pos):
                    volver_inicio(ventana, jugador)
                    return "inicio"
                elif boton_continuar.collidepoint(event.pos):
                    return "continuar" # Simplemente sale de la función para continuar con el juego

    
def reiniciar_nivel(jugador):
    jugador.score = 0  # Restablecer puntaje
    jugador.energia = 100  # Restablecer energía

def volver_inicio(ventana, jugador):
    ventana_inicio(ventana) # Se regresa a la ventana de inicio para comenzar nuevamente
    reiniciar_nivel(jugador) # Se vuelve a empezar el juego