import pygame
import math
import random

import codigo.constantes as constantes

class Weapon():    
    def __init__(self, image, imagen_disparo):
        # Se llama la imagen del disparo
        self.imagen_disparo = imagen_disparo
        # Se hace captura de la imagen
        self.imagen_original = image
        # Se establece una variable en donde se guarda el angulo
        self.angulo = 0
        # Se hace la rotación de dicha imagen
        self.imagen = pygame.transform.rotate(self.imagen_original, self.angulo)
        # Se encapsula la forma en un rectangulo
        self.forma = self.imagen.get_rect()
        # Accion de descargar
        self.descarga = False
        # Para dar un retraso de tiempo al ultimo disparo
        self.ultima_descarga = pygame.time.get_ticks()
        
        # Rango de ángulos permitidos
        self.min_angle = -45
        self.max_angle = 45
        
    # Rotación y posición del arma
    def update(self, personaje):
        descarga_cooldown = constantes.COOLDOWN_BALAS
        shot = None 
        self.forma.center = personaje.forma.center
        if personaje.flip == False:
            self.forma.x += personaje.forma.width/5.5
            self.forma.y += personaje.forma.height/3.9
            self.rotar(False)
        if personaje.flip == True:
            self.forma.x -= personaje.forma.width/5.5
            self.forma.y += personaje.forma.height/3.9
            self.rotar(True)
    
        # Mover escopeta con el mouse
        mouse_pos = pygame.mouse.get_pos()
        distancia_x = mouse_pos[0] - self.forma.centerx
        distancia_y = -(mouse_pos[1] - self.forma.centery)
        self.angulo = math.degrees(math.atan2(distancia_y, distancia_x))
        
        # Limitar ángulo dentro del rango permitido
        # self.angulo = max(self.min_angle, min(self.angulo, self.max_angle))
        
        # Deteccion de clicks del mouse
        if pygame.mouse.get_pressed()[0] and self.descarga == False and (pygame.time.get_ticks() - self.ultima_descarga >= descarga_cooldown): # El cero es el boton izquierdo
            shot = Shot(self.imagen_disparo, self.forma.centerx, self.forma.centery, self.angulo)
            self.descarga = True
            self.ultima_descarga = pygame.time.get_ticks()
            
        # Resetear el click del mouse
        if pygame.mouse.get_pressed()[0] == False:
            self.descarga = False
        return shot
        
    # Logica de rotación
    def rotar(self, rotar):
        if rotar == True:
            imagen_flip = pygame.transform.flip(self.imagen_original, True, False)
            self.imagen = pygame.transform.rotate(imagen_flip, self.angulo)
        else:
            imagen_flip = pygame.transform.flip(self.imagen_original, False, False)
            self.imagen = pygame.transform.rotate(imagen_flip, self.angulo)
     
    
    def dibujar(self, interfaz):
        interfaz.blit(self.imagen, self.forma)
    
class Shot(pygame.sprite.Sprite):
    # Poder dar uso de la clase constructor de Sprite
    def __init__(self, image, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.imagen_original = image
        self.angulo = angle
        self.image = pygame.transform.rotate(self.imagen_original,  self.angulo)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        # Calculo de la velocidad de disparo
        self.delta_x = math.cos(math.radians(self.angulo)) * constantes.VELOCIDAD_DISPARO
        self.delta_y = -math.sin(math.radians(self.angulo)) * constantes.VELOCIDAD_DISPARO
    
    def update(self, lista_enemigos):
        dano = 0
        posicion_dano = None
        
        self.rect.x += self.delta_x
        self.rect.y += self.delta_y
        
        # Ver si las balas salieron de pantalla
        if self.rect.right < 0 or self.rect.left > constantes.ANCHO_VENTANA or self.rect.top > constantes.ALTO_VENTANA:
            self.kill()
    
        # Verificacion de colisiones con enemigos
        for enemigo in lista_enemigos:
            if enemigo.forma.colliderect(self.rect):
                # Al disparar puede hacer daño la bala en el rango propuesto
                dano = 15 + random.randint(-7, 7)
                posicion_dano = enemigo.forma
                enemigo.energia -= dano 
                self.kill()
                break
            
        return dano, posicion_dano
            
    def dibujar(self, interfaz):
        interfaz.blit(self.image, (self.rect.centerx, self.rect.centery - int(self.image.get_height()/2)))
        
    