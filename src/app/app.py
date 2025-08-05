from fastapi import FastAPI, Depends
from inference import generate_answer
from pydantic import BaseModel
from sqlalchemy.orm import Session
import database
from database import Chats

app = FastAPI()
database.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.Session()
    try:
        yield db
    finally:
        db.close()

# Pydantic schema for input
class UserQuery(BaseModel):
    question: str


@app.post("/chat")
def user_query(query_text: UserQuery, db: Session = Depends(get_db)):
    # Generate answer
    answer = generate_answer(query_text.question)

    # Create model instance
    chat_entry = Chats(query=query_text.question, relevant_answers=answer)

    # Save to DB
    db.add(chat_entry)
    db.commit()
    db.refresh(chat_entry)

    return {"question": chat_entry.query, "answer": chat_entry.relevant_answers}

@app.get("/db/")
def read_users(db: Session = Depends(get_db)):
    return db.query(Chats).all()