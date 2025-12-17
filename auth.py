# auth.py

USERS = {
    "MCERA": {
        "password": "mcera@123",
        "role": "ADMIN"
    },
    "MCEAP": {
        "password": "mceap@123",
        "role": "STORE"
    }
}


def authenticate(username, password):
    user = USERS.get(username)
    if not user:
        return None

    if user["password"] == password:
        return user["role"]

    return None
