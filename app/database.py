import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = "postgresql://generacion01:d2$$4Gen@shortline.proxy.rlwy.net:31885/railway"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

metadata = MetaData()

Base = automap_base(metadata=metadata)

def init_db():
    metadata.reflect(engine)
    Base.prepare(autoload_with=engine)
    print("Tablas detectadas automáticamente:")
    for table_name in metadata.tables.keys():
        print(f"   - {table_name}")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_models():
    return Base.classes