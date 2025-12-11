import secrets

# Length parameter used to influence the number of bytes 
# for generating a secure, URL-safe secret key
key_length = 32

# Generates a cryptographically secure random string.
# token_urlsafe() returns a base64-url encoded string, safe for URLs and storage.
secret_key = secrets.token_urlsafe(key_length)

# Prints the generated secret key
print(secret_key)
