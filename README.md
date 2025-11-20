#FastAPI CRUD Backend

#Description
Backend API built with FastAPI and SQLAlchemy. Supports full CRUD operations, PATCH updates, and clean RESTful architecture.

#Tech Stack
- Python 3.11+
- FastAPI
- SQLAlchemy
- SQLite / MySQL
- Pydantic
- Annotated validation

#Endpoints
- POST /assignment/create/ — create a new assignment
- GET /assignment/ — get all assignments
- GET /assignment/{id}/ — get assignment by ID
- PUT /assignment/update/{id} — full update
- PATCH /assignment/update/some/{id} — partial update
- DELETE /assignment/delete/{id} — delete assignment

#Features
- Clean architecture
- JWT-ready structure (optional)
- Swagger UI for testing
- Modular codebase
  
#License
MIT License
