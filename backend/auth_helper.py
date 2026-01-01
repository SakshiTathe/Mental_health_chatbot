import bcrypt

# Function to hash a password
def hash_password(password: str) -> bytes:
    try:
        salt = bcrypt.gensalt(rounds=10)
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed
    except Exception as e:
        print("Error hashing password:", e)

# Function to compare password with hashed password
def compare_password(password: str, hashed_password: bytes) -> bool:
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
    except Exception as e:
        print("Error comparing passwords:", e)
        return False
