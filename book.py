# Import the FastAPI framework
from fastapi import FastAPI, Body

# Create a FastAPI app
app = FastAPI()

# Sample data for books
BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]

# Route to get all books
@app.get("/books")
def read_all_books():
    return BOOKS

# Route to get a specific book by its title
@app.get("/books/{book_title}")
def read_all_books(book_title: str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book

# Route to get books by author's name
@app.get("/books/authorname/getbook")
def get_the_book(authors: str):
    book_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == authors.casefold():
            book_to_return.append(book)
    return book_to_return

# Route to get books by a specific author
@app.get("/books/{author}/booksbyauthor")
def read_books(author: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == author.casefold():
            books_to_return.append(book)
    return books_to_return

# Route to get books by category
@app.get("/books/")
def read_query(category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return

# Route to get books by both author and category
@app.get("/books/{book_author}/")
async def read_author_category_by_query(book_author: str, category: str):
    books_to_return = []
    for book in BOOKS:
        if (
            book.get('author').casefold() == book_author.casefold()
            and book.get('category').casefold() == category.casefold()
        ):
            books_to_return.append(book)
    return books_to_return

# Route to create a book
@app.post("/books/create-book")
def create_book(book_title=Body()):
    return BOOKS.append(book_title)

# Route to update a book
@app.put("/books/update_book")
def update_book(update_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == update_book.get('title').casefold():
            BOOKS[i] = update_book

# Route to delete a book
@app.delete("/books/delete_book/{book_title}")
def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            BOOKS.pop(i)
            break
