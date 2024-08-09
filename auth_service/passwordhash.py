import bcrypt
print("Hello from Hash")

def hash_password(password):
    """Hash a password for use in user_auth"""
    salted_pw = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salted_pw)
    return hashed


def verify_password(stored_password, provided_password):
    """Check password"""
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password)

