import re

# Cargar lista de contraseñas débiles
with open('10k_most_common_passwords.txt') as f:
    weak_passwords = set(f.read().splitlines())

# Función para verificar si una contraseña es débil
def es_password_debil(password):
    return password in weak_passwords

# Función para verificar la validez de una contraseña según criterios de complejidad
def es_password_valido(password):
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    return True