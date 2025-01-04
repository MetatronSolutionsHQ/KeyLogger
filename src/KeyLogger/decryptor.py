from cryptography.fernet import Fernet

# Load the encryption key from the key file
key_file = "encryption_key.key"
with open(key_file, "rb") as f:
    key = f.read()

# Create the Fernet cipher object
cipher = Fernet(key)

# Replace this with the encrypted content you want to decrypt
encrypted_content = "gAAAAA..."  # Replace with actual encrypted data

# Decrypt the content
try:
    decrypted_message = cipher.decrypt(encrypted_content.encode()).decode()
    print("Decrypted Message:", decrypted_message)
except Exception as e:
    print(f"Error decrypting message: {e}")
