import os
from dotenv import load_dotenv

load_dotenv()

# JWT
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-secret-change-me")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

# Имена ролей в таблице role
ADMIN_ROLE = "Admin"
DEFAULT_ROLE = "User"
