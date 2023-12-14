import string
from random import SystemRandom
from django.utils.text import slugify

# Gerando letra aleatórias para utilizar no SLUG
def random_letters(k=5):
    return ''.join(SystemRandom().choices(
        string.ascii_letters + string.digits,
        k=k
    ))

# Gerando um texto recebido com letras aleatorias formando uma URL
def slugify_new(text, k=5):
    return slugify(text) + random_letters(k)