from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
from src.utils.settings import settings

Base = declarative_base()

engine = create_engine(url=settings.DB_CONNECTION)


LocalSession  = sessionmaker(bind=engine)

def get_db():
    session = LocalSession()
    try:
        yield session
    finally:
        session.close()

#engine = database k rasta(connection + pool)
# session = kaam krne k workspace
# bind-engine = workspace ko database k sath bind krna

# session khud database nhi janta . use ek engine k sath s bind krna pdta hai tbhi vo query bhej sakta hai

#  "bind=engine session factory ko database engine se jodta hai, taaki us factory se bane saare sessions usi database ke connection pool ke through queries chalayein."