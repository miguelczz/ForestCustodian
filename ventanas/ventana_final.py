import pygame
import codigo.constantes as constantes

def ventana_final(ventana, texto, fuente, color, ancho, alto):
    ventana_emergente = pygame.Surface((ancho, alto))
    ventana_emergente.fill(constantes.NEGRO)
    ventana_emergente.set_alpha(200)

    # Obtener las coordenadas de la ventana principal
    ventana_rect = ventana.get_rect()

    # Calcular la posición de la ventana emergente en la pantalla
    ventana_emergente_x = (ventana_rect.width - ancho) // 2
    ventana_emergente_y = (ventana_rect.height - alto) // 2

        # Dividir el texto en párrafos
    lineas = texto.split("\n")
    y_offset = 50  # Espaciado inicial desde la parte superior de la ventana emergente

    for linea in lineas:
        texto_superficie = fuente.render(linea, True, color)
        texto_rect = texto_superficie.get_rect(center=(ancho // 2, y_offset))
        ventana_emergente.blit(texto_superficie, texto_rect)
        y_offset += 30  # Espaciado entre líneas

    # Calcular las coordenadas del botón en relación con la ventana emergente
    boton_x = (ancho - 100) // 2  # Centrar horizontalmente
    boton_y = 270  # Centrar verticalmente
    boton_aceptar = pygame.Rect(boton_x, boton_y, 100, 43)
    pygame.draw.rect(ventana_emergente, constantes.ROJO, boton_aceptar)

    # Dibujar el texto en el botón
    boton_texto = fuente.render("Aceptar", True, constantes.BLANCO)
    boton_texto_rect = boton_texto.get_rect(center=boton_aceptar.center)
    ventana_emergente.blit(boton_texto, boton_texto_rect)

    # Dibujar la ventana emergente en el centro de la pantalla
    ventana.blit(ventana_emergente, (ventana_emergente_x, ventana_emergente_y))

    pygame.display.update()

    # Ajustar las coordenadas del botón para la detección de eventos
    boton_aceptar_evento = boton_aceptar.move(ventana_emergente_x, ventana_emergente_y)

    return boton_aceptar_evento
