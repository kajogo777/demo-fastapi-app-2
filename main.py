from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import get_db, Post, Base, engine
from pydantic import BaseModel
from typing import List


Base.metadata.create_all(bind=engine)


app = FastAPI()


class PostCreate(BaseModel):
    title: str
    content: str
    published: bool = True


class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    published: bool

    class Config:
        from_attributes = True


@app.get("/")
async def health_check():
    return {"status": "healthy"}


@app.post("/posts", response_model=PostResponse)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    new_post = Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/posts", response_model=List[PostResponse])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(Post).all()
    return posts
