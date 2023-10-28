from typing import Optional

from pydantic import BaseModel,Field
from fastapi import FastAPI, Path, Query, HTTPException
app = FastAPI()
from starlette import status

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class Bookrequest(BaseModel):
    id: Optional[int] = Field(None,title="Id is Not needed")
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int

    class Config:
        json_schema_extra = {'example':{'title': 'New book', 'author':'coding with Roby', 'description':'Fantastic', 'rating': 5, 'published_date': 2023}}


BOOKS = [Book(1, 'Computer Science Pro', 'coding with roby', 'Very Good',4.5,2023),Book(2, 'FastAPI', 'coding with roby', 'Good',5,2024),Book(3, 'Data Science', 'coding with eric', 'Very Good',5,2025),Book(4, 'Computer Science Pro', 'coding with roby', 'Very Good',4.5,2026)]


@app.get("/books", status_code=status.HTTP_200_OK)
def bookreturn():
    return BOOKS


@app.get("/books/{bookid}", status_code=status.HTTP_200_OK)
def getbookbyid(bookid:int = Path(gt=0)):
    for book in BOOKS:
        if bookid == book.id:
            return book
    raise HTTPException(status_code=404 , detail="Item Not Found")


@app.get("/book/", status_code=status.HTTP_200_OK)
def getbookbyrating(book_rating:int=Query(gt=0,lt=6)):
    bookstoappend = []
    for book in BOOKS:
        if book_rating == book.rating:
            bookstoappend.append(book)
    return bookstoappend


@app.get("/book/publishdate", status_code=status.HTTP_200_OK)
def getbookbydate(publishdate:int = Query(gt=1000,lt=2031)):
    bookstoappend=[]
    for book in BOOKS:
        if book.published_date == publishdate:
            bookstoappend.append(book)
    return bookstoappend


@app.post("/books/create-book", status_code=status.HTTP_201_CREATED)
def createbook(book_request:Bookrequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(findbookid(new_book))


def findbookid(book: BOOKS):
    book.id = 1 if len(BOOKS)==0 else BOOKS[-1].id+1
    # if len(BOOKS) > 0:
    #     book.id = BOOKS[-1].id+1
    # else:
    #     book.id=1
    return book


@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: Bookrequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_changed = True
    if not book_changed:
        raise HTTPException(status_code=404, detail='Item not found')



@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletebook(book_id:int = Path(gt=0)):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changed=True
            break
    if not book_changed:
        raise HTTPException(status_code=404 , detail="Item Not Found")