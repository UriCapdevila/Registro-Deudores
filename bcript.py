import bcrypt

# Contraseña original
password = "miclave123"

# Generar hash con salt automático
hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

# Convertir a string si lo vas a guardar en base de datos
hashed_pw_str = hashed_pw.decode('utf-8')
print("Hash generado:", hashed_pw_str)