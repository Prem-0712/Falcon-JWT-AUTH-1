from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from decouple import config

DB_USER = config("DB_USER")
DB_PASS = config("DB_PASS")
DB_NAME = config("DB_NAME")
DB_PORT = config("DB_PORT")

DATABASE_URL = f"mysql+aiomysql://{DB_USER}:{DB_PASS}@localhost:{DB_PORT}/{DB_NAME}"

engine = create_async_engine(DATABASE_URL, echo=True, future=True)

SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)
