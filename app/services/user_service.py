from app.models.user import UserInDB
from app.core.security import verify_password

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$NSXwHNTGqk8wkZsZblQHT.ECd49EaKFnA6nbnDgz3KQuNpFl6QG4O",
        "disabled": False,
    }
}

def get_user(db, username: str):
    if username in db:
        return UserInDB(**db[username])

def authenticate_user(fake_db, username: str, password: str):
    print("username=",username)
    user = get_user(fake_db, username)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user
