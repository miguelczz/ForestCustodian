import pygame
import random

import codigo.constantes as constantes
from codigo.items import Item

# Definición de listas de tiles específicos para ciertos comportamientos
obstaculos = [81]
obstaculos_2 = [78, 36, 37, 66, 67]
arboles = [22, 23]
exit_tiles = [44]
final = [84]
puerta_cerrada = [36, 37, 66, 67]

class Mundo:
    def __init__(self):
        self.map_tiles = []
        self.obstaculos_tiles = []
        self.lista_arboles = []
        self.tiles = []
        self.lista_item = []
        self.exit_tile = []
        self.final_tile = []
        self.puertas_cerradas_tiles = []
        
    def process_data(self, world_data, tile_list, item_imagenes, nivel):
        for layer in world_data:
            for y, row in enumerate(layer):
                for x, tile in enumerate(row):
                    if tile != -1:
                        image = tile_list[tile]
                        self.tiles.append((image, (x * constantes.TILE_SIZE, y * constantes.TILE_SIZE)))
                        image_rect = image.get_rect()
                        image_x = x * constantes.TILE_SIZE
                        image_y = y * constantes.TILE_SIZE
                        image_rect.center = (image_x, image_y)
                        tile_data = [image, image_rect, image_x, image_y, tile]

                        # Agregar tiles a obstáculos basados en el nivel
                        if (nivel == 1 and tile in obstaculos) or (nivel == 2 and tile in obstaculos_2):
                            self.obstaculos_tiles.append(tile_data)

                        elif nivel == 2 and tile in final:
                            self.final_tile.append(tile_data)

                        elif tile in puerta_cerrada:
                            self.puertas_cerradas_tiles.append(tile_data)

                        elif tile in exit_tiles:
                            self.exit_tile.append(tile_data)

                        elif tile in arboles:
                            self.lista_arboles.append(tile_data)

                        elif tile == 91:
                            basura_imagen = random.choice([item_imagenes[0], item_imagenes[1], item_imagenes[2], item_imagenes[3], item_imagenes[4]])  # Selección aleatoria
                            basura = Item(image_x, image_y, 0, basura_imagen)  
                            self.lista_item.append(basura)
                            tile_data[0] = tile_list[17]

                        elif tile == 14:
                            posion = Item(image_x, image_y, 1, item_imagenes[5]) 
                            self.lista_item.append(posion)
                            tile_data[0] = tile_list[17]

                        self.map_tiles.append(tile_data)

    def cambiar_puerta(self, jugador, tile_list):
        buffer = 50
        # Cuando el jugador esté a la proximidad del rectángulo podrá abrir la puerta
        proximidad_rect = pygame.Rect(jugador.forma.x - buffer, jugador.forma.y - buffer, jugador.forma.width + 2 * buffer, jugador.forma.height + 2 * buffer)

        for tile_data in self.map_tiles:
            image, rect, x, y, tile_type = tile_data
            if proximidad_rect.colliderect(rect):
                if tile_type in puerta_cerrada:
                    if tile_type == 36 or tile_type == 66:
                        new_tile_type = 57
                    elif tile_type == 37 or tile_type == 67:
                        new_tile_type = 58

                    tile_data[-1] = new_tile_type
                    tile_data[0] = tile_list[new_tile_type]

                    # Eliminar el tile de la lista de colisiones
                    if tile_data in self.obstaculos_tiles:
                        self.obstaculos_tiles.remove(tile_data)

                    return True
        return False

    def update(self, posicion_pantalla):
        for tile in self.map_tiles:
            tile[2] += posicion_pantalla[0]
            tile[3] += posicion_pantalla[1]
            tile[1].center = (tile[2], tile[3])

    def draw(self, surface):
        for tile in self.map_tiles:
            surface.blit(tile[0], tile[1])

    def verificar_final(self, jugador_rect):
        for tile_data in self.final_tile:
            if tile_data[1].colliderect(jugador_rect):
                return True
        return False
