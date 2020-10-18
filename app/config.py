from starlette.config import Config

config = Config(".env")

JWT_EXP: int = 60 * 24 * 365  # 365 days while debug
JWT_ALG: str = config("ALGORITHM")
JWT_SECRET: str = config("SECRET_KEY")

DATABASE_URL = config("DATABASE_URL")
