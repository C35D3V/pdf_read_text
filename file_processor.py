import os
import fitz  # PyMuPDF para manejo robusto de PDFs
import pytesseract  # Tesseract para OCR
from PIL import Image, ImageOps, ImageEnhance  # Para manipulación de imágenes
import io
from multiprocessing import Pool
from settings import config # Archivo de configuración para parámetros globales

# -----------------------------
# FUNCIONES DE PREPROCESAMIENTO
# -----------------------------

def preprocess_image(image):
    """
    Preprocesa una imagen antes de realizar OCR para mejorar los resultados.
    - Escala de grises.
    - Aumento de contraste.
    - Binarización (blanco y negro).
    - Redimensionado condicional (aumentar resolución solo si es necesario).
    """
    try:
        image = ImageOps.grayscale(image)  # Convertimos a escala de grises
        image = ImageEnhance.Contrast(image).enhance(2.0)  # Aumentamos el contraste
        image = image.convert("L").point(lambda x: 255 if x > 128 else 0, mode="1")  # Binarización

        # Redimensionamos solo si el ancho o alto son menores a un umbral
        if image.width < 1000 or image.height < 1000:
            image = image.resize((image.width * 2, image.height * 2), Image.Resampling.LANCZOS)
        return image
    except Exception as e:
        print(f"Error durante el preprocesamiento de la imagen: {e}")
        return image  # Devolvemos la imagen sin modificaciones si ocurre un error


# -----------------------------
# FUNCIONES DE OCR
# -----------------------------

def perform_ocr(image):
    """
    Realiza OCR en una imagen utilizando Tesseract.
    """
    try:
        preprocessed_image = preprocess_image(image)  # Preprocesamos la imagen
        text = pytesseract.image_to_string(preprocessed_image, lang=config.DEFAULT_LANGUAGE)
        if text.strip():
            print("Texto extraído con Tesseract.")
            return text
    except Exception as e:
        print(f"Error con Tesseract OCR: {e}")

    return "No se pudo extraer texto de la imagen."


# -----------------------------
# FUNCIONES DE MANEJO DE PDFs
# -----------------------------

def extract_text_with_fitz(pdf_path):
    """
    Extrae texto embebido de un archivo PDF utilizando PyMuPDF (fitz).
    """
    extracted_text = ""
    doc = fitz.open(pdf_path)
    for page in doc:
        extracted_text += page.get_text("text")  # Extracción de texto usando PyMuPDF
    return extracted_text


def extract_images_from_pdf(pdf_path):
    """
    Extrae imágenes de un PDF utilizando PyMuPDF.
    """
    images = []
    try:
        doc = fitz.open(pdf_path)
        for page in doc:
            for img_index, img in enumerate(page.get_images(full=True)):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_data = base_image["image"]
                try:
                    image = Image.open(io.BytesIO(image_data))
                    images.append(image)
                except Exception as e:
                    print(f"Error al procesar una imagen extraída: {e}")
    except Exception as e:
        print(f"Error al extraer imágenes del PDF: {e}")
    return images


# -----------------------------
# FUNCIONES DE PROCESAMIENTO EN PARALELO
# -----------------------------

def process_image_parallel(image):
    """
    Función que maneja el OCR de manera paralela para cada imagen.
    """
    preprocessed_image = preprocess_image(image)
    text = pytesseract.image_to_string(preprocessed_image, lang=config.DEFAULT_LANGUAGE)
    return text


def process_images_in_parallel(images):
    """
    Procesa imágenes en paralelo para extraer texto utilizando OCR.
    """
    results = []
    with Pool(processes=os.cpu_count()) as pool:
        results = pool.map(process_image_parallel, images)
    return results


# -----------------------------
# FLUJO PRINCIPAL
# -----------------------------

def process_pdf_with_images(pdf_path):
    """
    Procesa un archivo PDF para extraer texto embebido y texto de imágenes.
    Optimiza el manejo de imágenes y utiliza procesamiento paralelo.
    """

    # Extraer texto embebido
    embedded_text = extract_text_with_fitz(pdf_path)

    # Si ya se ha extraído texto, no intentamos OCR en las imágenes
    if embedded_text.strip():
        print("Texto embebido extraído correctamente del PDF.")
        return embedded_text

    # Extraer imágenes
    images = extract_images_from_pdf(pdf_path)

    # Si no se extrajo texto embebido, procesar imágenes con OCR en paralelo
    print("Procesando imágenes en paralelo...")
    ocr_texts = process_images_in_parallel(images)

    # Combinar resultados de OCR
    ocr_text = "\n".join(ocr_texts)

    # Combinar resultados finales
    if embedded_text.strip() or ocr_text.strip():
        combined_text = f"[Texto embebido extraído del PDF]\n{embedded_text}\n\n[Texto extraído de imágenes]\n{ocr_text}"
    else:
        combined_text = "No se pudo extraer texto del PDF ni realizar OCR en las imágenes."

    return combined_text
