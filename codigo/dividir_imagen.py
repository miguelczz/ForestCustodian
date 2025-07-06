from PIL import Image
import os

def dividir_guardar_imagen(ruta_imagen, carpeta_destino, divisiones_por_columna):
    
    # Carga de imagen
    img = Image.open(ruta_imagen)
    
    ancho, alto = img.size
    
    # Calcular el número de divisiones por fila para mantener la forma cuadrada
    tamano_cuadrado = ancho // divisiones_por_columna
    divisiones_por_fila = alto // tamano_cuadrado
    
    # Crear carpeta de destino si no existe
    os.makedirs(carpeta_destino, exist_ok=True)
    
    # Dividir la imagen y guardar cada tile
    contador = 0
    for i in range(divisiones_por_fila):
        for j in range(divisiones_por_columna):
            # Coordenadas del cuadrado
            izquierda = j * tamano_cuadrado
            superior = i * tamano_cuadrado
            derecha = izquierda + tamano_cuadrado
            inferior = superior + tamano_cuadrado
            
            # Cortar y guardar el cuadrado
            cuadrado = img.crop((izquierda, superior, derecha, inferior))
            nombre_archivo = f"tile ({contador+1}).png"
            cuadrado.save(os.path.join(carpeta_destino, nombre_archivo))
            
            contador += 1

# Ejemplo de uso
dividir_guardar_imagen(ruta_imagen="assets/images/tiles/Forest_Tileset.png", carpeta_destino="assets/images/tiles/", divisiones_por_columna=16)
