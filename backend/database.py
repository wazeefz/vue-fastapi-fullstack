from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL ='postgresql://millaridzuan:Miso2706$@localhost/fastapi_db'
# DATABASE_URL_AIAGENT ='postgresql://millaridzuan:Miso2706$@localhost/books_db'

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()