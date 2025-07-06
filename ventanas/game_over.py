import pygame

import codigo.constantes as constantes
from ventanas.inicio import ventana_inicio

def mostrar_game_over(ventana):
    
    # Ajusta el tamaño de la fuente
    fuente = pygame.font.Font("assets/fonts/mago3.ttf", 60)
    
    # Texto Game Over y obtencion del rectangula para posicionarlo   
    game_over_texto = fuente.render("Game Over...", True, constantes.ROJO)
    game_over_rect = game_over_texto.get_rect(center=(constantes.ANCHO_VENTANA // 2, constantes.ALTO_VENTANA // 2 - 100))
    
    game_over_ventana = pygame.Surface((constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA))
    game_over_ventana.fill(constantes.NEGRO)
    game_over_ventana.blit(game_over_texto, game_over_rect)
    ventana.blit(game_over_ventana, (0, 0))
    
    pygame.display.update()

def botones(ventana, font, jugador, lista_enemigos):
    
    # Botón para reiniciar nivel
    boton_reiniciar = pygame.Rect(200, 430, 200, 50) # Modificar tamaño y posicion de botones
    pygame.draw.rect(ventana, constantes.VERDE, boton_reiniciar)
    reiniciar_texto = font.render("Reiniciar Nivel", True, constantes.BLANCO)
    ventana.blit(reiniciar_texto, (220, 440)) # Posicion del texto
    
    # Botón para volver al inicio
    boton_inicio = pygame.Rect(500, 430, 200, 50) # Modificar tamaño y posicion de botones
    pygame.draw.rect(ventana, constantes.AZUL, boton_inicio)
    inicio_texto = font.render("Inicio", True, constantes.BLANCO)
    ventana.blit(inicio_texto, (570, 440)) # Posicion del texto
    
    pygame.display.update()

    while True:
        # Se les da funcionalidad a los botones
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Llama a la función para reiniciar nivel
                if boton_reiniciar.collidepoint(event.pos):
                    reiniciar_nivel(jugador, lista_enemigos)
                    return "reiniciar"
                # Llama a la función para volver al inicio
                elif boton_inicio.collidepoint(event.pos):
                    volver_inicio(ventana, jugador, lista_enemigos)  
                    return "reiniciar"
    
def reiniciar_nivel(jugador, lista_enemigos):
    jugador.x = 170  # Posición inicial en x
    jugador.y = 200  # Posición inicial en y
    jugador.score = 0  # Restablecer puntaje
    jugador.energia = 100  # Restablecer energía
    
    lista_enemigos.clear()

def volver_inicio(ventana, jugador, lista_enemigos):
    ventana_inicio(ventana) # Se regresa a la ventana de inicio para comenzar nuevamente
    reiniciar_nivel(jugador, lista_enemigos) # Se vuelve a empezar el juego
