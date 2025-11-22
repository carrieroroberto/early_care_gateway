import secrets
key_length = 32
secret_key = secrets.token_urlsafe(key_length)
print(secret_key)