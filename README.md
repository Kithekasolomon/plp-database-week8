# plp-database-week8

Library Management System API
A FastAPI-based CRUD application for managing a library's books and members, connected to a MySQL database.
Prerequisites

Python 3.8+
MySQL Server
pip (Python package manager)

Setup Instructions

Clone the repository:
git clone <repository-url>
cd library-management-api


Install dependencies:
pip install -r requirements.txt


Set up the MySQL database:

Create a MySQL database and run the SQL script (library_management.sql) to set up the schema.
Update the database connection details in main.py (e.g., DATABASE_URL).


Run the application:
uvicorn main:app --reload

The API will be available at http://localhost:8000.


API Endpoints
Books

Create Book: POST /books/
Body: { "title": "string", "isbn": "string", "publication_year": integer, "author_id": integer, "available_copies": integer }
Response: Book details


Get All Books: GET /books/
Response: List of all books


Get Book by ID: GET /books/{book_id}
Response: Book details


Update Book: PUT /books/{book_id}
Body: { "title": "string", "isbn": "string", "publication_year": integer, "author_id": integer, "available_copies": integer }
Response: Updated book details


Delete Book: DELETE /books/{book_id}
Response: Success message



Members

Create Member: POST /members/
Body: { "first_name": "string", "last_name": "string", "email": "string", "join_date": "YYYY-MM-DD", "phone": "string" }
Response: Member details


Get All Members: GET /members/
Response: List of all members


Get Member by ID: GET /members/{member_id}
Response: Member details


Update Member: PUT /members/{member_id}
Body: { "first_name": "string", "last_name": "string", "email": "string", "join_date": "YYYY-MM-DD", "phone": "string" }
Response: Updated member details


Delete Member: DELETE /members/{member_id}
Response: Success message



Database Schema
The database schema is defined in library_management.sql. It includes tables for Authors, Books, Members, and Loans with appropriate relationships and constraints.
Notes

Ensure the MySQL server is running before starting the application.
The API uses SQLAlchemy for ORM and Pydantic for data validation.
Interactive API documentation is available at http://localhost:8000/docs.
