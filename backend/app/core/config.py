from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str
    debug: bool
    database_url: str
    secret_key: str

    class Config:
        env_file = ".env"


settings = Settings()




#  python -m uvicorn app.main:app --reload
