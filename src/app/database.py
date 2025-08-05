from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, String, Integer

engine = create_engine("sqlite:///Rag.db", connect_args = {'check_same_thread' : False})
Session = sessionmaker(autocommit = False, autoflush = False, bind = engine)
Base = declarative_base()

class Chats(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True)
    query = Column(String, nullable=False)
    relevant_answers = Column(String, nullable=False)

if __name__ == '__main__':
    pass