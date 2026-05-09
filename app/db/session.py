from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.db.settings import config

DATABASE_URL = f'postgresql+psycopg2://{config.USER}:{config.PASSWORD}@{config.HOST}:{config.PORT}/{config.DATABASE}'

engine = create_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,
    echo=False,
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)

Base = declarative_base()