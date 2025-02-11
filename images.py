import logging
import urllib
import urllib.request

import cloudinary
import cloudinary.uploader
from sqlalchemy import create_engine, text

table_name = "cards"
engine = create_engine("postgresql+psycopg2://admin:1234@localhost/root")

logger = logging.getLogger(__name__)
logging.basicConfig(filename="cards.log", encoding="utf-8", level=logging.DEBUG)

# Configurar Cloudinary
cloudinary.config(
    cloud_name="dhryf7mwa", api_key="858658663754912", api_secret="u7QJn4wBa4IM2rKoIVIhhn7cQxM"
)


def add_log(message):
    logger.error(message)


def subir_imagen_a_cloudinary(url_gcs, card_id):
    """Descarga una imagen desde Google Cloud y la sube a Cloudinary."""
    filename = "prueba.jpg"
    try:
        urllib.request.urlretrieve(url_gcs, filename)

        result = cloudinary.uploader.upload(filename)
        print(f"Imagen subida: {result['secure_url']}")
        return result["secure_url"]
    except Exception:
        add_log(f"Error al descargar la imagen con url: {url_gcs} ID: {card_id}.")
        return None


def change_image_cards():
    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT id, image FROM {table_name}")).fetchall()
        for row in result:
            card_id, card_image = row
            url_cloudinary = subir_imagen_a_cloudinary(card_image, card_id)
            if url_cloudinary:
                stmt = text(f"UPDATE {table_name} SET image = :new_image WHERE id = :id")
                conn.execute(stmt, {"new_image": url_cloudinary, "id": card_id})
                conn.commit()


# Esto se usa para cargar imagenes rn masa desde BBDD
# change_image_cards()
# URL de prueba (reemplázala con la que tienes) Esta parte se usa para cargar imagenes de una en una
url_google_cloud = "https://storage.googleapis.com/materiahunter-prod.appspot.com/images/cards/PR/PR-065_8-018R.jpg"
url_cloudinary = subir_imagen_a_cloudinary(url_google_cloud, 3213)
