from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

SQLALCHEMY_DATABASE_URL = settings.database_url
engine = create_engine(SQLALCHEMY_DATABASE_URL, future=True)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
