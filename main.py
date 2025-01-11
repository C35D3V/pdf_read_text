import os
from file_processor import process_pdf_with_images  # Para procesar PDF con texto e imágenes
from utils import save_text_to_file  # Para guardar el texto extraído
from settings import config # Archivo de configuración para parámetros globales

MAX_ATTEMPTS = 3

def show_menu():
    print("\n--- MENÚ PRINCIPAL ---")
    print("1. Procesar un archivo (PDF o Imagen)")
    print("2. Configuración")
    print("3. Salir")
    print("----------------------")


def process_file_option():
    print("\n¿Quieres procesar un solo archivo o una carpeta completa?")
    print("1. Procesar un solo archivo.")
    print("2. Procesar una carpeta completa.")

    option = input("Selecciona una opción (1-2): ")

    if option == '1':
        process_single_file()
    elif option == '2':
        process_folder()
    else:
        print("\nOpción inválida. Volverás al menú principal.")
        return


def process_single_file():
    attempts = 0
    while attempts < MAX_ATTEMPTS:
        file_path = input("Introduce la ruta del archivo (PDF o imagen): ")
        try:
            extracted_text = process_pdf_with_images(file_path)  # Procesamos el archivo
        except Exception as e:
            print(f"Error al procesar el archivo: {e}")
            attempts += 1
            if attempts == MAX_ATTEMPTS:
                print("\nHas superado el número máximo de intentos. Volverás al menú principal.")
                return
            continue

        print("\nTexto extraído:")
        print(extracted_text)
        save = input("\n¿Deseas guardar el texto en un archivo de texto? (s/n): ")
        if save.lower() == 's':
            file_name = input("Introduce el nombre del archivo para guardar el texto: ")
            try:
                save_text_to_file(extracted_text, file_name)
                print("\nTexto guardado con éxito. Volverás al menú principal.")
            except Exception as e:
                print(f"Error al guardar el archivo: {e}")
            return
        else:
            print("\nNo se ha guardado el texto. Volverás al menú principal.")
            return


def process_folder():
    folder_path = input("Introduce la ruta de la carpeta: ")
    if not os.path.isdir(folder_path):
        print("La ruta proporcionada no es una carpeta válida. Volverás al menú principal.")
        return

    extracted_texts = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if file_path.lower().endswith(('.pdf', '.jpg', '.jpeg', '.png', '.bmp', '.gif')):
            print(f"\nProcesando el archivo: {filename}")
            try:
                extracted_text = process_pdf_with_images(file_path)
                extracted_texts.append((filename, extracted_text))
            except Exception as e:
                print(f"Error al procesar {filename}: {e}")

    if extracted_texts:
        print("\n--- Resultados de la extracción ---")
        for filename, text in extracted_texts:
            print(f"\nTexto extraído de {filename}:")
            print(text)
            save = input(f"\n¿Deseas guardar el texto de {filename} en un archivo de texto? (s/n): ")
            if save.lower() == 's':
                file_name = input(f"Introduce el nombre del archivo para guardar el texto de {filename}: ")
                try:
                    save_text_to_file(text, file_name)
                    print(f"\nTexto de {filename} guardado con éxito.")
                except Exception as e:
                    print(f"Error al guardar el texto de {filename}: {e}")
    else:
        print("\nNo se encontraron archivos compatibles en la carpeta proporcionada.")


def configuration_option():
    print("\n--- CONFIGURACIÓN ---")
    print("Actualmente, no hay configuraciones disponibles para modificar.")
    print("Esta sección será mejorada en futuras versiones.")
    print("Volverás al menú principal.")


def main():
    while True:
        show_menu()
        option = input("Por favor, selecciona una opción (1-3): ")
        if option == '1':
            process_file_option()
        elif option == '2':
            configuration_option()
        elif option == '3':
            print("\nGracias por usar el programa. ¡Hasta luego!")
            break
        else:
            print("\nOpción inválida. Por favor, selecciona una opción válida.")


if __name__ == '__main__':
    main()
