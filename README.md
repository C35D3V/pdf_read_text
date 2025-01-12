# PDF Text Extractor.

Este proyecto es un script en Python diseñado para extraer texto de archivos PDF e imágenes, utilizando OCR (Reconocimiento Óptico de Caracteres) con Tesseract. Además, es capaz de manejar archivos individuales o carpetas completas, optimizando el rendimiento mediante procesamiento paralelo.

## 🚀 Características.

- **Extracción de texto de PDFs:** Utiliza PyMuPDF (fitz) para obtener texto embebido.
- **OCR en Imágenes:** Aplica OCR a imágenes extraídas de PDFs o proporcionadas directamente.
- **Procesamiento paralelo:** Maneja múltiples imágenes al mismo tiempo para mejorar la velocidad.
- **Preprocesamiento de imágenes:** Mejora los resultados del OCR mediante escalas de grises, aumento de contraste, y binarización.
- **Soporte para múltiples idiomas:** Configurable para español e inglés por defecto.

## 🛠 Requisitos.

- Python 3.x
- Tesseract OCR instalado en el sistema
- Dependencias listadas en `requirements.txt`

### Instalación de Tesseract.
En sistemas basados en Arch Linux (como EndeavourOS), instala Tesseract con:
```bash
sudo pacman -S tesseract tesseract-data-eng tesseract-data-spa
```
En sistemas basados en Ubuntu, instala Tesseract con:
```bash
sudo apt update
sudo apt install tesseract-ocr tesseract-ocr-eng tesseract-ocr-spa
```
## ⚙️ Configuración.

El archivo config.py contiene parámetros globales que puedes ajustar:

DEFAULT_LANGUAGE = 'spa+eng'  # Idioma predeterminado para OCR
DEFAULT_OUTPUT_FOLDER = 'output/'  # Carpeta donde se guardarán los resultados

## 🚀 Uso.
- Configura un entorno virtual (opcional pero recomendado):
```bash
python -m venv env
source env/bin/activate  # En Linux/MacOS
env\Scripts\activate     # En Windows
```
- Instala las dependencias:
```bash
pip install -r requirements.txt
```
- Ejecuta el script:
```bash
python main.py
```
- Sigue las instrucciones en pantalla para seleccionar un archivo o carpeta para procesar.

## 💾 Salida.
- Los textos extraídos se guardan en la carpeta configurada en DEFAULT_OUTPUT_FOLDER (por defecto output/).
- Puedes personalizar el nombre del archivo de salida.

## 🐞 Solución de Problemas.
- Error de "ModuleNotFoundError": Asegúrate de que todas las dependencias estén instaladas:
```bash
pip install -r requirements.txt
```
- Tesseract no funciona: Verifica que Tesseract esté correctamente instalado y configurado en tu sistema.

## 📃 Licencia.
Este proyecto está bajo la Licencia MIT. Puedes consultarla en el archivo LICENSE.

## 🤝 Contribuciones.
¡Las contribuciones siempre son bienvenidas! Si tienes ideas, mejoras o encuentras errores, por favor abre un issue o envía un pull request.
