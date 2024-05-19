from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text
from flask_login import UserMixin

class Base(DeclarativeBase):
    pass

db=SQLAlchemy(model_class=Base)

class FoodPost(db.Model):
    __tablename__="posts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    author_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"))
    author=relationship("User",back_populates="posts")
    title : Mapped[str] = mapped_column(String, nullable=False)
    subtitle: Mapped[str] = mapped_column(String, nullable=True)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)
    comments=relationship("Comment",back_populates="post")

class User(db.Model,UserMixin):
    __tablename__='users'
    id:Mapped[int]=mapped_column(Integer,primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    password: Mapped[str] = mapped_column(String(1000),nullable=False)
    posts=relationship("FoodPost",back_populates="author")
    comments=relationship("Comment",back_populates="author")

class Comment(db.Model):
    __tablename__="comments"
    id:Mapped[int]=mapped_column(Integer,primary_key=True)
    author_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"))
    post_id:Mapped[int]=mapped_column(Integer,db.ForeignKey("posts.id"))
    author = relationship("User", back_populates="comments")
    text:Mapped[str]=mapped_column(Text,nullable=False)
    post=relationship("FoodPost",back_populates="comments")