import hashlib

password = "miclave123"
hashed_pw = hashlib.sha256(password.encode()).hexdigest()
print(hashed_pw)