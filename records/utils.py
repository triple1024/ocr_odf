from pdf2image import convert_from_path
from PIL import Image
import pytesseract


def pdf_to_images(pdf_path):
    images =convert_from_path(pdf_path)
    return images

def image_to_text(image, coordinates):
    cropped_image = image.crop(coordinates)
    text = pytesseract.image_to_string(cropped_image)
    return text