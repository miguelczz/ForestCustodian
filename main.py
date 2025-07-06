import pygame
import pygame.image
import math
import sys
import csv
import os

import codigo.constantes as constantes
from codigo.personaje import Personaje
from codigo.mundo import Mundo
from codigo.weapon import Weapon
from codigo.textos import DamageText
from ventanas.permanentes import solicitar_nombre, guardar_puntaje
from ventanas.victoria import mostrar_victoria, botones_victoria
from ventanas.game_over import mostrar_game_over, botones
from ventanas.ventana_final import ventana_final

#? Funciones -------------------------------

# Se hace la escala en cada imagen
def escalar_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    nueva_imagen = pygame.transform.scale(image, size=(int(w*scale), int(h*scale)))
    return nueva_imagen

# Se hace delimitacion con comas en cada fila
def cargar_mapa(filename):
    map_data = []
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            map_data.append([int(val) for val in row])
    return map_data

# Se usa la fuente para la puntuacion
def dibujar_texto(texto, fuente, color, x, y):
    img = fuente.render(texto, True, color)
    ventana.blit(img, (x, y))
    
# Funcion para contar elementos
def contar_elementos(directorio):
    # El os entre a la ruta entregada y devuelve los elementos que hay dentro de ella
    return len(os.listdir(directorio))

# Funcion enlistar elementos
def nombres_carpetas(directorio):
    # El os entre a la ruta entregada y devuelve los elementos que hay dentro de ella
    return os.listdir(directorio)

# Funcion vida del jugador
def vida_jugador(ventana, jugador):
    for i in range(4):
        if jugador.energia >= ((i+1) * 25):
            ventana.blit(corazon_lleno, (2 + i * 50, 5))
        elif jugador.energia >= i * 25:
            ventana.blit(corazon_medio, (2 + i * 50, 5))
        else:
            ventana.blit(corazon_vacio, (2 + i * 50, 5))
            
# Funcion para reiniciar el nivel
def reiniciar_nivel():
    global enemigo_creado, enemigo_derrotado, lista_enemigos, jugador, enemigo_reaparicion, tiempo_reaparicion
    enemigo_creado = False
    enemigo_derrotado = False
    lista_enemigos = []
    jugador.energia = 100
    enemigo.energia = 100
    enemigo_reaparicion = True
    tiempo_reaparicion = pygame.time.get_ticks()
    
# Se deja vacio el mundo    
def resetear_mundo():
    grupo_damage_text.empty()
    grupos_disparos.empty()
    grupo_items.empty()

# Precarga de todos los tiles antes de ejecutar la imagen del mundo    
def cargar_tiles(tipo, cantidad):
    tile_list = []
    for i in range(1, cantidad + 1):
        tile_image = pygame.image.load(f"assets//images//tiles//tiles_{tipo}//tile ({i}).png")
        tile_image = pygame.transform.scale(tile_image, (constantes.TILE_SIZE, constantes.TILE_SIZE))
        tile_list.append(tile_image)
    return tile_list
  
#? Basicos ----------------------------
  
# Inicialización de la librería
pygame.init()

# Creacion de la ventana
ventana = pygame.display.set_mode((constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA))

# Fuentes
font = pygame.font.Font("assets/fonts/mago3.ttf", 30)

# Nombre del juego
pygame.display.set_caption("Forest Custodian")

# Variables
posicion_pantalla = [0, 0]
nivel = 1
nivel_2_inicio = None  # Variable para almacenar el tiempo de inicio del nivel 2
tiempo_mensaje_intro = 500
tiempo_espera_enemigo = 6000  # Tiempo en milisegundos
enemigo_reaparicion = False 

#? Musica ----------------------------

sonido_disparo = pygame.mixer.Sound("assets/sounds/shot/shot2.mp3")
    
musica_victoria = pygame.mixer.Sound("assets/sounds/win/win (1).mp3")

musica_perder = pygame.mixer.Sound("assets/sounds/lose/lose (1).mp3")

sonido_recoger = pygame.mixer.Sound("assets/sounds/pickup/pickup.mp3")

musica_fondo = pygame.mixer.Sound("assets/sounds/background/background3.mp3")

musica_fondo_2 = pygame.mixer.Sound("assets/sounds/background/background (2).mp3")


#? Mapa Principal ----------------------------

# Carga de imagenes del mundo
tile_list = cargar_tiles(1, constantes.TILE_TIPES)

for x in range(constantes.TILE_TIPES):
    tile_image = [pygame.image.load(f"assets//images//tiles//tiles_1//tile ({x+1}).png") for x in range(constantes.TILE_TIPES)]
    tile_image = [pygame.transform.scale(img, (constantes.TILE_SIZE, constantes.TILE_SIZE)) for img in tile_image]

# Cargar todas las capas del mapa
world_data = [cargar_mapa(f"niveles/nivel_1/ForestMapa ({i}).csv") for i in range(1, 4)]  # Iteracion de las capas
world = Mundo()

#? Objetos ----------------------------
        
# Carga de imagen de los items
banana = pygame.image.load("assets/images/items/basura/banana.png")
banana = escalar_img(banana, scale=0.2)

botella = pygame.image.load("assets/images/items/basura/botella.png")
botella = escalar_img(botella, scale=0.08)

manzana = pygame.image.load("assets/images/items/basura/manzana.png")
manzana = escalar_img(manzana, scale=0.08)

posion = pygame.image.load("assets/images/items/potion/potion.png")
posion = escalar_img(posion, scale=0.07)

lata = pygame.image.load("assets/images/items/basura/lata.png")
lata = escalar_img(lata, scale=0.07)

bolsa = pygame.image.load("assets/images/items/basura/bolsa.png")
bolsa = escalar_img(bolsa, scale=0.08)

item_imagenes = [[manzana], [banana], [lata], [bolsa], [botella], [posion]]

# Energia
corazon_vacio = pygame.image.load("assets/images/items/corazones/corazon_vacio.png").convert_alpha()
corazon_vacio = escalar_img(corazon_vacio, constantes.SCALA_CORAZON)
corazon_medio = pygame.image.load("assets/images/items/corazones/corazon_medio.png").convert_alpha()
corazon_medio = escalar_img(corazon_medio, constantes.SCALA_CORAZON)
corazon_lleno = pygame.image.load("assets/images/items/corazones/corazon_lleno.png").convert_alpha()
corazon_lleno = escalar_img(corazon_lleno, constantes.SCALA_CORAZON)
            
world.process_data(world_data, tile_image, item_imagenes, nivel=1)
            
# Creacion de grupos de sprites
grupo_items = pygame.sprite.Group()

# Añadir items desde la data del nivel
for item in world.lista_item:
    grupo_items.add(item)

# Arma
imagen_escopeta = pygame.image.load("assets/images/weapons/gun.png")
imagen_escopeta = escalar_img(imagen_escopeta, constantes.SCALA_ARMA)

# Disparo
imagen_disparo = pygame.image.load("assets/images/weapons/shot.png")
imagen_disparo = escalar_img(imagen_disparo, constantes.SCALA_DISPARO)

# Crear un arma de la clase weapon
escopeta = Weapon(imagen_escopeta, imagen_disparo)

# Crear un grupo de sprites
grupo_damage_text = pygame.sprite.Group()
grupos_disparos = pygame.sprite.Group()

#? Personajes ----------------------------

#! JUGADOR

# Se crean dos variables para que se ejecute la simulacion de caminar o estar quieto
jugador_estatico = [escalar_img(pygame.image.load(f"./assets/images/characters/player/Ranger_Idle_{i}.png"), constantes.SCALA_PERSONAJE) for i in range(1, 3)]
jugador_caminando = [escalar_img(pygame.image.load(f"./assets/images/characters/player/Ranger_Walk_{i}.png"), constantes.SCALA_PERSONAJE) for i in range(1, 3)]

# Crear un jugador de la clase personaje
jugador = Personaje(x=320, y=1250, animaciones=jugador_estatico, tipo=1, energia=100, rango=5)

# Definir las variables de movimiento del jugador
mover_arriba = False
mover_abajo = False
mover_izquierda = False
mover_derecha = False

# Calcular el movimiento del jugador
delta_x = 0
delta_y = 0

# Controlacion del frame rate
reloj = pygame.time.Clock()

# Funcionalidad de si esta moviendose o se esta quieto el personaje
jugador_moviendo = False

#! ENEMIGO

# Se crean  variables para que se ejecute la simulacion de caminar o estar quieto
enemigo_quieto = [escalar_img(pygame.image.load(f"assets/images/characters/enemy/Idle/Idle ({i}).png"), constantes.SCALA_ENEMIGO) for i in range(1, 6+1)]   
enemigo_f_quieto = [escalar_img(pygame.image.load(f"assets/images/characters/final_enemy/Idle/Idle ({i}).png"), constantes.SCALA_ENEMIGO_2) for i in range(1, 4+1)]
   
enemigo_caminando = [escalar_img(pygame.image.load(f"assets/images/characters/enemy/Walk/Walk ({i}).png"), constantes.SCALA_ENEMIGO) for i in range(1, 8+1)]   
enemigo_f_caminando = [escalar_img(pygame.image.load(f"assets/images/characters/final_enemy/Walk/Walk ({i}).png"), constantes.SCALA_ENEMIGO_2) for i in range(1, 4+1)]

# Crear un enemigo de la clase personaje
enemigo = Personaje(x=400, y=300, animaciones=enemigo_quieto, tipo=2, energia=100, rango=constantes.RANGO)
enemigo_final = Personaje(x=400, y=300, animaciones=enemigo_f_quieto, tipo=2, energia=100, rango=constantes.RANGO_2)

# Crear enemigos
lista_enemigos = []

# Rastrear si el enemigo ya ha sido creado
enemigo_creado = False
enemigo_moviendo = False
enemigo_derrotado = False

mensaje_molino = False
ventana_mostrada = False
mostrar_ventana_inicio = True

texto_volumen = True
tiempo_texto_volumen = 0
duracion_texto_volumen = 4000
temp_mensaje_musica = None

# Reproducir música en bucle
musica_fondo.play(-1)
musica_fondo.set_volume(constantes.VOLUMEN)

#* Programa principal ----------------------------

temp_mensaje_musica = pygame.time.get_ticks()
run = True
while run:
    
    #? Generales -------------------------
    
    # Se establece que vaya a 60 FPS
    reloj.tick(constantes.FPS)
    
    # Limpia la pantalla
    if nivel == 1:
        ventana.fill(constantes.COLOR_BG)
        if texto_volumen:
            tiempo_transcurrido = pygame.time.get_ticks()
            if tiempo_transcurrido - temp_mensaje_musica <= duracion_texto_volumen:
                dibujar_texto("Usa UP/DOWN para ajustar el volumen.", font, (255, 255, 255), 500, 300)
        else:
            texto_volumen = False 
            
        # Se actualiza el temporizador del mensaje de volumen
        temp_mensaje_musica = pygame.time.get_ticks()
        
    elif nivel == 2:
        ventana.fill(constantes.COLOR_BG_2)
    
    for event in pygame.event.get():
        # En el momento en que run sea falso se cerrará el juego
        if event.type == pygame.QUIT:
            run = False
                
        # Presionar la q para salir
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_UP:
                constantes.VOLUMEN = min(1.0, constantes.VOLUMEN + 0.1)
                musica_fondo.set_volume(constantes.VOLUMEN)
                musica_fondo_2.set_volume(constantes.VOLUMEN)  # Agregar esta línea
            elif event.key == pygame.K_DOWN:
                constantes.VOLUMEN = max(0.0, constantes.VOLUMEN - 0.1)
                musica_fondo.set_volume(constantes.VOLUMEN)
                musica_fondo_2.set_volume(constantes.VOLUMEN)  # Agregar esta línea

    #? Jugador --------------------------
            
            # Movimiento del personaje con teclas a, d, w, s
            if event.key == pygame.K_w:
                mover_arriba = True
            if event.key == pygame.K_s:
                mover_abajo = True
            if event.key == pygame.K_a:
                mover_izquierda = True
            if event.key == pygame.K_d:
                mover_derecha = True
            if event.key == pygame.K_r:
                if world.cambiar_puerta(jugador, tile_list):
                    print(" ")
                
        # Movimiento del personaje al soltar las teclas
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                mover_arriba = False
            if event.key == pygame.K_s:
                mover_abajo = False
            if event.key == pygame.K_a:
                mover_izquierda = False
            if event.key == pygame.K_d:
                mover_derecha = False

    # Calcular el movimiento del jugador
    delta_x = 0
    delta_y = 0

    # Mover al personaje solo si hay un cambio en las teclas presionadas
    if mover_arriba or mover_abajo or mover_izquierda or mover_derecha:
        jugador_moviendo = True
        enemigo_moviendo = True
        delta_x = (mover_derecha - mover_izquierda) * constantes.VELOCIDAD
        delta_y = (mover_abajo - mover_arriba) * constantes.VELOCIDAD
    else:
        jugador_moviendo = False
        enemigo_moviendo = False
    
    # Mover al personaje
    posicion_pantalla, nivel_completado = jugador.movimiento(delta_x, delta_y, world.obstaculos_tiles, world.exit_tile)
        
    # Actualizacion en la animacion del jugador
    if jugador_moviendo:
        jugador.animaciones = jugador_caminando
        enemigo.animaciones = enemigo_caminando
        enemigo_final.animaciones = enemigo_f_caminando
    else:
        jugador.animaciones = jugador_estatico
        enemigo.animaciones = enemigo_quieto
        enemigo_final.animaciones = enemigo_f_caminando
        
    #* Llamados -----------------------
        
    # Se dibuja el mundo
    world.draw(ventana)
    
    # Se actualiza la parte del mapa en dependencia de la posicion del jugador
    world.update(posicion_pantalla)
    
     # Actualizacion del estado del jugador
    jugador.update()
    
    # Se dibuja al jugador en la ventana
    jugador.dibujar(ventana) 
    
    # Chequear si el nivel esta completado
    if nivel_completado == True:
        nivel += 1
        resetear_mundo()
        musica_fondo.stop()
        musica_fondo_2.play()
        
        if nivel == 2:
            nivel_2_inicio = pygame.time.get_ticks()  # Almacena el tiempo actual en milisegundos
        
        # Carga de imagenes del segundo mundo
        tile_list = cargar_tiles(2, constantes.TILE_TIPES_2)

        # Cargar todas las capas del segundo mapa
        world = Mundo()
        world_data = [cargar_mapa(f"niveles/nivel_{nivel}/ForestMapa ({i}).csv") for i in range(1, 4)] # Iteracion de las capas
        world.process_data(world_data, tile_list, item_imagenes, nivel=2)
        jugador.actualizar_coordenadas(constantes.COORDENADAS[str(nivel)])

    
    if jugador.score >= 200 and not enemigo_creado:
        # Crear un enemigo solo si no hay enemigos actualmente en la lista        
        if not lista_enemigos:
            lista_enemigos.append(enemigo)
            enemigo_creado = True     
            
    # Verificar si ha pasado el tiempo suficiente para crear el enemigo en el nivel 2        
    elif nivel == 2 and not lista_enemigos and not enemigo_reaparicion:
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - nivel_2_inicio >= tiempo_mensaje_intro:
            dibujar_texto(f"Bienvenido a la guarida", font, constantes.BLANCO, 600, 50)
            dibujar_texto(f"del jefe de las basuras!", font, constantes.BLANCO, 600, 70)
        if tiempo_actual - nivel_2_inicio >= tiempo_mensaje_intro + 2000:
            dibujar_texto(f"Derrotalo para acabar", font, constantes.BLANCO, 600, 100)       
            dibujar_texto(f"con su horrible imperio.", font, constantes.BLANCO, 600, 120)       
                 
        if tiempo_actual - nivel_2_inicio >= tiempo_espera_enemigo:
            lista_enemigos.append(enemigo_final)
            enemigo_creado = True     
        
    # Renderización del Game Over
    if jugador.energia <= 0:
        musica_fondo.stop()
        musica_perder.play()  # Reproduce la música al perder
        
        # Se llama a la función solicitar_nombre para obtener el nombre del jugador
        nombre_jugador = solicitar_nombre(ventana, font)
        guardar_puntaje(nombre_jugador, jugador.score, nivel)
        
        
        mostrar_game_over(ventana)
        game_over = botones(ventana, font, jugador, lista_enemigos)

        if enemigo in lista_enemigos:
            lista_enemigos.remove(enemigo_final)
            lista_enemigos.remove(enemigo)
        
        if game_over == "reiniciar":
            reiniciar_nivel()  # Reiniciar el nivel
            musica_fondo.play(-1)
            jugador.score = 0
            
            
    # Verificar si es tiempo de reaparición del enemigo
    if enemigo_reaparicion:
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - tiempo_reaparicion >= 3000:
            enemigo_reaparicion = False

    # Dibujar y actualizar el enemigo solo si ya ha sido creado
    if enemigo_creado and not enemigo_reaparicion:
        for ene in lista_enemigos:
                
            if ene.energia > 0:
                ene.update()
                ene.dibujar(ventana)
                ene.enemigos(jugador, world.obstaculos_tiles, posicion_pantalla, world.lista_arboles, world.exit_tile)
            
            else:
                lista_enemigos.remove(ene)
                enemigo_derrotado = True
                musica_victoria.play()
                
                if nivel == 1:
                    mensaje_molino = True
                    ene.energia = 100
                elif nivel == 2:
                    ene.energia = 0
                    tiempo_muerte_vikingo = pygame.time.get_ticks()
                    
                    reiniciar_nivel()
                
            # Verificar distancia y talar árboles si está fuera del rango
            distancia = math.hypot(jugador.forma.centerx - ene.forma.centerx, jugador.forma.centery - ene.forma.centery)
            
            if distancia > constantes.RANGO and nivel == 1:
                ene.talar_arboles(jugador, world)        
    
    if nivel == 2 and enemigo_final.energia <= 0:
        dibujar_texto(f"Ahora tienes acceso al cofre,", font, constantes.BLANCO, 330, 10)
        dibujar_texto(f"buscalo y dirigite a el!", font, constantes.BLANCO, 360, 30)
        musica_fondo_2.stop()
        
        tiempo_transcurrido = pygame.time.get_ticks() - tiempo_muerte_vikingo
        
        if tiempo_transcurrido >= 4000:
            # Mostrar el mensaje "Presiona (e) para continuar."
            dibujar_texto(f"Presiona (R) para avanzar.", font, constantes.BLANCO, 600, 570)
        
        resetear_mundo()
        reiniciar_nivel() 
            
    if nivel == 1 and enemigo_derrotado:
        lista_enemigos.clear()
        musica_fondo.stop()
        mostrar_victoria(ventana)
        decision_jugador = botones_victoria(ventana, font, jugador)
        
        if decision_jugador == "continuar":
            mensaje_molino = True
            
            # Carga de imagenes del mundo
            tile_list = cargar_tiles(1, constantes.TILE_TIPES)

            # Cargar todas las capas del mapa
            world_data = [cargar_mapa(f"niveles/nivel_1/molino/ForestMapa ({i}).csv") for i in range(1, 4)] # Iteracion de las capas
            world = Mundo()
            world.process_data(world_data, tile_image, item_imagenes, nivel)
            jugador.actualizar_coordenadas([320, 1250])
            musica_fondo.play(-1)
             
        elif decision_jugador == "reiniciar" or decision_jugador == "inicio":
            mensaje_molino = False  
            reiniciar_nivel()
            jugador.score = 0
            musica_fondo.play(-1)
            
    if not ventana_mostrada:    
        # Verificar si el jugador derrotó al enemigo del nivel 2
        if world.verificar_final(jugador.forma):
            # Mostrar la ventana emergente
            # Texto que se mostrará en la ventana final, con párrafos separados por \n
            texto_final = "Felicidades guerrero!\n\nAprendiste el gran valor\nde preservar nuestra naturaleza.\n\nGracias por jugar."
            boton_rect = ventana_final(ventana, texto_final, font, (255, 255, 255), 420, 350)
            
            ventana_mostrada = True
            
            # Esperar a que el jugador presione el botón "Aceptar"
            ventana_final_abierta = True
            while ventana_final_abierta:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        ventana_final_abierta = False             
                        run = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if boton_rect.collidepoint(event.pos):
                            ventana_final_abierta = False
                            nombre_jugador = solicitar_nombre(ventana, font)
                            # Guarda el puntaje del jugador utilizando el nombre obtenido
                            guardar_puntaje(nombre_jugador, jugador.score, nivel)

        # Una vez cerrada la ventana emergente, continuar el juego normalmente
        enemigo_derrotado = False  
           
    if mensaje_molino and nivel == 1:
        dibujar_texto(f"Busca el molino!", font, constantes.BLANCO, 670, 40)
        resetear_mundo()
        
    # Actualizacion del estado del arma
    disparo = escopeta.update(jugador)
    
    if disparo:
        grupos_disparos.add(disparo)
        sonido_disparo.play()   
    for disparo in grupos_disparos:
        damage, posicion_dano = disparo.update(lista_enemigos)
        if damage:
            damage_text = DamageText(posicion_dano.centerx, posicion_dano.centery, str(damage), font, constantes.ROJO)
            grupo_damage_text.add(damage_text)
         
    # Dibujar corazones
    vida_jugador(ventana, jugador) 
        
    # Se dibuja la escopeta
    escopeta.dibujar(ventana)
    
    # Dibujar disparos
    for shot in grupos_disparos:
        shot.dibujar(ventana)
        
    # Actualizacion del daño
    grupo_damage_text.update()
        
    # Dibujar textos
    grupo_damage_text.draw(ventana)
    
    # Actualizacion de items
    grupo_items.update(posicion_pantalla, jugador, grupo_items)
  
    # Se dibujan los items
    grupo_items.draw(ventana)

    # Letrero de puntaje
    
    if nivel == 1:
        dibujar_texto(f"Nivel: {str(nivel)}", font, constantes.BLANCO, 650, 10)
        dibujar_texto(f"Puntaje: {jugador.score}", font, constantes.BLANCO, 760, 10)
    else: 
        dibujar_texto(f"Nivel: {str(nivel)}", font, constantes.BLANCO, 790, 10)
        
    # Actualiza la pantalla
    pygame.display.update() 
    
    # Detener la música
    pygame.mixer.music.stop()

pygame.quit()