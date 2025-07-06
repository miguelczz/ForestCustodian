import pygame
import codigo.constantes as constantes

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, item_type, animacion_list):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.animacion_list = animacion_list
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.animacion_list[self.frame_index]
        self.sonido_recoger = pygame.mixer.Sound("assets/sounds/pickup/pickup.mp3")
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.visible = True

    def update(self, posicion_pantalla, personaje, grupo_items):
        if self.visible:
            # Reposicionamiento del item basado en la posición de la cámara
            self.rect.x += posicion_pantalla[0]
            self.rect.y += posicion_pantalla[1]

            # Comprobar colisión entre el personaje y el item
            if self.rect.colliderect(personaje.forma):
                if self.item_type == 0:
                    personaje.score += constantes.PUNTOS
                    self.sonido_recoger.play()
                elif self.item_type == 1:
                    personaje.energia += 30
                    if personaje.energia > 100:
                        personaje.energia = 100

                self.visible = False  # Ocultar el objeto al ser recogido
                grupo_items.remove(self)  # Quitar el objeto del grupo de items

            # Actualizar la animación del item
            cooldown_animacion = 100
            if pygame.time.get_ticks() - self.update_time > cooldown_animacion:
                self.frame_index += 1
                self.update_time = pygame.time.get_ticks()

            if self.frame_index >= len(self.animacion_list):
                self.frame_index = 0

            self.image = self.animacion_list[self.frame_index]

    def draw(self, surface):
        if self.visible:
            surface.blit(self.image, self.rect)
