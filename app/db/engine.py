from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker

from app.core.settings import settings

SQLALCHEMY_DATABASE_URL_OBJ = URL.create(
    drivername=" postgresql+psycopg2",
    database="postgresql",
    username=settings.db_username,
    host=settings.db_hostname,
    password=settings.db_password,
    port=settings.db_port,
)

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.db_username}:{settings.db_password}@{settings.db_hostname}:{settings.db_port}/{settings.db_name}"


# for burmese language
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,
)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)
