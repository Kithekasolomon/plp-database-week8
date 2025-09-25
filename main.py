from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import date
from typing import Optional

# Database connection
DATABASE_URL = "mysql+mysqlconnector://root:86663@slomon/library_management"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# FastAPI app
app = FastAPI()

# Pydantic models
class BookBase(BaseModel):
    title: str
    isbn: str
    publication_year: Optional[int] = None
    author_id: Optional[int] = None
    available_copies: int = 1

class Book(BookBase):
    book_id: int

class MemberBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    join_date: date
    phone: Optional[str] = None

class Member(MemberBase):
    member_id: int

# SQLAlchemy models
class BookDB(Base):
    __tablename__ = "Books"
    book_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    isbn = Column(String(13), unique=True, nullable=False)
    publication_year = Column(Integer)
    author_id = Column(Integer)
    available_copies = Column(Integer, nullable=False, default=1)

class MemberDB(Base):
    __tablename__ = "Members"
    member_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    join_date = Column(Date, nullable=False)
    phone = Column(String(15))

# CRUD Operations
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/books/", response_model=Book)
def create_book(book: BookBase):
    db = SessionLocal()
    db_book = BookDB(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    db.close()
    return db_book

@app.get("/books/", response_model=list[Book])
def read_books():
    db = SessionLocal()
    books = db.query(BookDB).all()
    db.close()
    return books

@app.get("/books/{book_id}", response_model=Book)
def read_book(book_id: int):
    db = SessionLocal()
    book = db.query(BookDB).filter(BookDB.book_id == book_id).first()
    db.close()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, book: BookBase):
    db = SessionLocal()
    db_book = db.query(BookDB).filter(BookDB.book_id == book_id).first()
    if db_book is None:
        db.close()
        raise HTTPException(status_code=404, detail="Book not found")
    for key, value in book.dict().items():
        setattr(db_book, key, value)
    db.commit()
    db.refresh(db_book)
    db.close()
    return db_book

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    db = SessionLocal()
    db_book = db.query(BookDB).filter(BookDB.book_id == book_id).first()
    if db_book is None:
        db.close()
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(db_book)
    db.commit()
    db.close()
    return {"message": "Book deleted"}

@app.post("/members/", response_model=Member)
def create_member(member: MemberBase):
    db = SessionLocal()
    db_member = MemberDB(**member.dict())
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    db.close()
    return db_member

@app.get("/members/", response_model=list[Member])
def read_members():
    db = SessionLocal()
    members = db.query(MemberDB).all()
    db.close()
    return members

@app.get("/members/{member_id}", response_model=Member)
def read_member(member_id: int):
    db = SessionLocal()
    member = db.query(MemberDB).filter(MemberDB.member_id == member_id).first()
    db.close()
    if member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    return member

@app.put("/members/{member_id}", response_model=Member)
def update_member(member_id: int, member: MemberBase):
    db = SessionLocal()
    db_member = db.query(MemberDB).filter(MemberDB.member_id == member_id).first()
    if db_member is None:
        db.close()
        raise HTTPException(status_code=404, detail="Member not found")
    for key, value in member.dict().items():
        setattr(db_member, key, value)
    db.commit()
    db.refresh(db_member)
    db.close()
    return db_member

@app.delete("/members/{member_id}")
def delete_member(member_id: int):
    db = SessionLocal()
    db_member = db.query(MemberDB).filter(MemberDB.member_id == member_id).first()
    if db_member is None:
        db.close()
        raise HTTPException(status_code=404, detail="Member not found")
    db.delete(db_member)
    db.commit()
    db.close()
    return {"message": "Member deleted"}
