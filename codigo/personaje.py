import math
import pygame
import codigo.constantes as constantes

class Personaje():
    def __init__(self, x, y, animaciones, tipo, energia, rango):
        self.energia = energia
        self.vivo = True
        self.score = 0
        self.flip = False
        self.animaciones = animaciones
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.animaciones[self.frame_index]
        self.forma = self.image.get_rect()
        self.forma.center = (x, y)
        self.tipo = tipo 
        self.golpe = False
        self.ultimo_golpe = pygame.time.get_ticks()
        self.rango = rango

    def actualizar_coordenadas(self, tupla):
        self.forma.center = (tupla[0], tupla[1])

    def movimiento(self, delta_x, delta_y, obstaculos_tiles, exit_tile):
        posicion_pantalla = [0, 0]
        nivel_completado = False

        if delta_x < 0:
            self.flip = True
        if delta_x > 0:
            self.flip = False

        self.forma.x += delta_x
        for obstacle in obstaculos_tiles:
            if obstacle[1].colliderect(self.forma):
                if delta_x > 0:
                    self.forma.right = obstacle[1].left
                if delta_x < 0:
                    self.forma.left = obstacle[1].right

        self.forma.y += delta_y
        for obstacle in obstaculos_tiles:
            if obstacle[1].colliderect(self.forma):
                if delta_y > 0:
                    self.forma.bottom = obstacle[1].top
                if delta_y < 0:
                    self.forma.top = obstacle[1].bottom

        if self.tipo == 1:
            for tile in exit_tile:
                if tile[1].colliderect(self.forma):
                    nivel_completado = True

            if self.forma.right > (constantes.ANCHO_VENTANA - constantes.LIMITE_PANTALLA):
                posicion_pantalla[0] = (constantes.ANCHO_VENTANA - constantes.LIMITE_PANTALLA) - self.forma.right
                self.forma.right = constantes.ANCHO_VENTANA - constantes.LIMITE_PANTALLA
                
            if self.forma.left < constantes.LIMITE_PANTALLA:
                posicion_pantalla[0] = constantes.LIMITE_PANTALLA - self.forma.left
                self.forma.left = constantes.LIMITE_PANTALLA 

            if self.forma.bottom > (constantes.ALTO_VENTANA - constantes.LIMITE_PANTALLA):
                posicion_pantalla[1] = (constantes.ALTO_VENTANA - constantes.LIMITE_PANTALLA) - self.forma.bottom
                self.forma.bottom = constantes.ALTO_VENTANA - constantes.LIMITE_PANTALLA
                
            if self.forma.top < constantes.LIMITE_PANTALLA:
                posicion_pantalla[1] = constantes.LIMITE_PANTALLA - self.forma.top
                self.forma.top = constantes.LIMITE_PANTALLA 

            return posicion_pantalla, nivel_completado

        return posicion_pantalla, nivel_completado

    def enemigos(self, jugador, obstaculos_tiles, posicion_pantalla, lista_arboles, exit_tile):
        ene_dx = 0
        ene_dy = 0

        self.forma.x += posicion_pantalla[0]
        self.forma.y += posicion_pantalla[1]

        distancia = math.sqrt(((self.forma.centerx - jugador.forma.centerx)**2) + ((self.forma.centery - jugador.forma.centery)**2))

        if distancia < self.rango:
            if self.forma.centerx > jugador.forma.centerx:
                ene_dx = -constantes.VELOCIDAD_ENEMIGO
            if self.forma.centerx < jugador.forma.centerx:
                ene_dx = constantes.VELOCIDAD_ENEMIGO
            if self.forma.centery > jugador.forma.centery:
                ene_dy = -constantes.VELOCIDAD_ENEMIGO
            if self.forma.centery < jugador.forma.centery:
                ene_dy = constantes.VELOCIDAD_ENEMIGO
        else:
            arbol_mas_cercano = None
            distancia_arbol_mas_cercano = float('inf')
            for arbol in lista_arboles:
                distancia_arbol = math.sqrt(((self.forma.centerx - arbol[2])**2) + ((self.forma.centery - arbol[3])**2))
                if distancia_arbol < distancia_arbol_mas_cercano:
                    distancia_arbol_mas_cercano = distancia_arbol
                    arbol_mas_cercano = arbol

            if arbol_mas_cercano:
                if self.forma.centerx > arbol_mas_cercano[2]:
                    ene_dx = -constantes.VELOCIDAD_ENEMIGO
                if self.forma.centerx < arbol_mas_cercano[2]:
                    ene_dx = constantes.VELOCIDAD_ENEMIGO
                if self.forma.centery > arbol_mas_cercano[3]:
                    ene_dy = -constantes.VELOCIDAD_ENEMIGO
                if self.forma.centery < arbol_mas_cercano[3]:
                    ene_dy = constantes.VELOCIDAD_ENEMIGO

        if abs(ene_dx) < constantes.MIN_VELOCIDAD_ENEMIGO:
            ene_dx = constantes.MIN_VELOCIDAD_ENEMIGO if ene_dx >= 0 else -constantes.MIN_VELOCIDAD_ENEMIGO
        if abs(ene_dy) < constantes.MIN_VELOCIDAD_ENEMIGO:
            ene_dy = constantes.MIN_VELOCIDAD_ENEMIGO if ene_dy >= 0 else -constantes.MIN_VELOCIDAD_ENEMIGO

        self.movimiento(ene_dx, ene_dy, obstaculos_tiles, exit_tile)

        if distancia < constantes.RANGO_ATAQUE and not jugador.golpe:
            jugador.energia -= 20  
            jugador.golpe = True
            jugador.ultimo_golpe = pygame.time.get_ticks()   

    def talar_arboles(self, jugador, world):
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.ultimo_golpe > 1000:  # 1 segundo entre golpes
            self.ultimo_golpe = tiempo_actual
            jugador.energia -= 10

    def update(self):
        if self.energia <= 0:
            self.energia = 0
            self.vivo = False

        golpe_cooldown = 1000
        if self.tipo == 1 and self.golpe:
            if pygame.time.get_ticks() - self.ultimo_golpe > golpe_cooldown:
                self.golpe = False

        ANIMACION_COOLDOWN = 300
        if pygame.time.get_ticks() - self.update_time > ANIMACION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index = (self.frame_index + 1) % len(self.animaciones)
            self.image = self.animaciones[self.frame_index]

    def dibujar(self, interfaz):
        image_flip = pygame.transform.flip(self.image, self.flip, False)
        interfaz.blit(image_flip, self.forma)
