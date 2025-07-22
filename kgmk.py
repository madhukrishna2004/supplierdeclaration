import secrets

# Generate a secure random secret key
secret_key = secrets.token_hex(32)  # Generates a 32-byte (64 characters) hex string
print(f"Your secret key is: {secret_key}")
