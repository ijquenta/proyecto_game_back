import string  # Para trabajar con cadenas de caracteres
import random  # Para generar valores aleatorios

EXTENSIONS_PDF = {'pdf'}
EXTENSIONS_IMG = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in EXTENSIONS_PDF

def allowed_file_img(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in EXTENSIONS_IMG

def stringAleatorio(length=10):
    letters = string.ascii_letters
    random_string = ''.join(random.choice(letters) for _ in range(length))
    return random_string