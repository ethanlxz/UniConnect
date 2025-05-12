import string
import random
import re


# Utility function to generate a 6-character alphanumeric verification code
def generate_random_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

