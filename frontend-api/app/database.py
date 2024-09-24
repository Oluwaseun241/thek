# SqlAlchemy Import
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Own Import
from models import Base

SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/library_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
