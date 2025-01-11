import os  # Para manejar rutas de archivos

# Función para guardar texto en un archivo
def save_text_to_file(text, file_name):
    """
    Guarda el texto extraído en un archivo dentro de la carpeta "output".
    """
    try:
        # Aseguramos que la carpeta "output" exista
        if not os.path.exists('output'):
            os.makedirs('output')  # Creamos la carpeta si no existe
        # Guardamos el archivo en la carpeta "output"
        with open(f"output/{file_name}", 'w', encoding='utf-8') as file:
            file.write(text)
        print(f"Texto guardado exitosamente en output/{file_name}")
    except Exception as e:
        print(f"Error al guardar el archivo: {e}")  # Mostramos cualquier error al guardar
