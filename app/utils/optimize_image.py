from PIL import Image
# import piexif

# Función para optimizar las imagenes subidas al sistema
def optimize_image(file_stream, output_path, max_size=(200, 200), quality=85):
    image = Image.open(file_stream)
    image.thumbnail(max_size, Image.LANCZOS)
    
    # Detectar el formato de la imagen basado en la extensión del archivo.
    original_format = image.format  # PIL detecta el formato al abrir la imagen.
    
    if original_format in ['JPEG', 'JPG']:
        image = image.convert('RGB')  # Convertir a RGB para asegurar compatibilidad con JPEG
        image.save(output_path, 'JPEG', quality=quality, optimize=True, progressive=True)
    elif original_format == 'PNG':
        image.save(output_path, 'PNG', optimize=True)
    else:
        image.save(output_path, original_format) # Guardar en el formato original si no es ni JPEG ni PNG