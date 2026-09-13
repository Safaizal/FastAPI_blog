from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./blog.db" #this is where we change in order to change our database and the file mention in this line will automatically created.

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # this is factory method that creates the database sessions, each database gets it's own session


class Base(DeclarativeBase):
    pass


def get_db():
    with SessionLocal() as db:
        yield db #it's generator that cleanup and match the db session to our routes
