from sqlmodel import Session
from backend.app.db import engine
from backend.app.models.user import UserCreate
from backend.app.api.auth import register

# Create a test user
user_data = UserCreate(
    email="directtest@example.com",
    password="password123",
    full_name="Direct Test User"
)

try:
    with Session(engine) as session:
        result = register(user_data, session)
        print(f"Success! User created: {result.email}, ID: {result.id}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
