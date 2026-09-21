Let’s start by initializing it with uv.
uv is one of the fastest package managers I use: `uv add "fastapi[standard]"`
Note: don’t forget the closing quote.

Create `main.py` in the project folder and write the code to start the app.

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
	return {"message": "Hello World"}
```

Since FastAPI handles synchronous functions well, you can use async when you need it.

`uv run fastapi dev main.py`

You can also use `fastapi run`, but there is one difference: in `dev`, the site reloads automatically; in `run`, it does not.

After running the app, you can see the response. FastAPI also generates docs for your API—just add `/docs` or `/redoc` after your `localhost` URL to see them.

`@app.get("/")` is a decorator used to define a route.

In this code, the response is JSON. If you want an HTML response, import `HTMLResponse` from `fastapi.responses` and pass it as `response_class`, e.g. `@app.get("/", response_class=HTMLResponse)`.
Note: don’t forget to return an HTML string.

You can also map multiple endpoints to a single function by stacking decorators.

```python
@app.get("/", response_class=HTMLResponse)
@app.get("/posts", response_class=HTMLResponse)
```

You can visit the docs to verify you’ll see two endpoints with the same response. If, for some reason, you don’t want an endpoint to show up in the docs, you can use `include_in_schema=False` in the decorator.

This hides your endpoint from the docs, but you can still access it.

Use some dummy data and play with it.

## Day 2

We saw how to send an HTML response from an API. But if you’re building a website, writing HTML inside Python strings becomes painful. For that, you can use Jinja2 templates, which let you render data dynamically in HTML pages.

### 1. Template Setup

Import `Jinja2Templates` and initialize it by pointing to your `templates/` directory (03:27).

python
from fastapi.templating import Jinja2Templates
from fastapi import Request

templates = Jinja2Templates(directory="templates")

### 2. Serving Templates

Update your route to accept a `Request` object and return a `TemplateResponse` (06:11).

```jsx

@app.get("/", name="home",include_in_schema=False)

def home(request: Request):
	posts = [...] # Your data source
	return templates.TemplateResponse(request=request,"home.html",{"posts": posts, "title": "Home"}
)
```

### 3. Template Inheritance

Use a parent `layout.html` to define reusable structure. Child templates (like `home.html`) extend this layout using blocks (13:42).

**layout.html:**
html
{% block content %}{% endblock %}

**home.html:**
html
{% extends "layout.html" %}
{% block content %}
{% for post in posts %}

{% endfor %}
{% endblock %}

### 4. Static Files

Mount static assets (CSS, JS, images) so they are accessible via a URL path (24:13).

```jsx
from fastapi.staticfiles import StaticFiles

app.mount("/static", StaticFiles(directory="static"), name="static")
```

Use `{{ url_for('static', path='css/main.css') }}` in your HTML to link these files dynamically, if we change mount directory it will automatically rearrange it.

## Day 3

1. Understanding Path Parameters (1:25 - 2:02)

Path parameters allow you to capture specific values directly from the URL. Instead of fixed routes, you can define variables in the URL path using curly braces {}.

2. Implementing Dynamic API Endpoints (2:18 - 5:55)

To capture a value, define it in your path and pass it as an argument to your function. FastAPI uses Python type hints for automatic validation.

Example:
python
@app.get("/api/posts/{post_id}")
def get_post(post_id: int):

# FastAPI validates that post_id is an integer

for post in posts:
if post.get("id") == post_id:
return post

# Manual handling for missing data

1. Proper Error Handling with HTTPExceptions (6:57 - 10:31)

Instead of returning plain dictionaries for errors, use HTTPException and the status module to return standard RESTful status codes (e.g., 404 Not Found).

python
from fastapi import HTTPException, status

raise HTTPException(
status_code=status.HTTP_404_NOT_FOUND,
detail="Post not found"
)
4. Template Routes and Dynamic Links (12:41 - 20:21)

For rendering HTML templates, you pass the specific resource retrieved via the path parameter. Use url_for in your Jinja2 templates to keep links dynamic.

HTML snippet:
html
5. Custom Exception Handlers (23:17 - 34:00)

To provide a professional user experience, you can create separate exception handlers that check if a request is coming from an API (return JSON) or a web browser (return HTML).

```
RequestValidationError: Automatically caught when input types don't match the required type hint (e.g., passing a string where an integer is expected).
Starlette HTTP Exception: Used to catch global 404 errors beyond the FastAPI routes.
```

# Day4

**Pydantic schemas** in *FastAPI* to enforce data validation, improve documentation, and handle request/response serialization.

### 1. Why Use Pydantic?

- **Automatic Validation:** It uses Python type hints to enforce constraints at runtime (0:58).
- **Documentation:** *FastAPI* uses these models to auto-generate interactive API documentation (2:03).
- **Separation of Concerns:** Schemas define the API contract (in/out), while database models handle storage (1:37).

### 2. Creating Schemas (`schemas.py`)

We define models using `BaseModel` and `Field` for constraints like `min_length` (3:47).

python
from pydantic import BaseModel, Field, ConfigDict

class PostBase(BaseModel):
title: str = Field(min_length=1, max_length=100)
content: str = Field(min_length=1)
author: str = Field(min_length=1, max_length=50)

class PostCreate(PostBase):
pass  # Inherits fields for requests

class PostResponse(PostBase):
id: int
date_posted: str
model_config = ConfigDict(from_attributes=True) # Allows reading objects via dot notation

### 3. Integrating with FastAPI (`main.py`)

Use `response_model` to enforce the output structure and define request body types (11:33).

python
from fastapi import FastAPI, status
from schemas import PostCreate, PostResponse

app = FastAPI()

@app.post("/api/posts", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(post: PostCreate):
# Logic to handle post creation...
return new_post

@app.get("/api/posts", response_model=list[PostResponse])
def get_posts():
return posts

### 4. Key Takeaways

- **`from_attributes=True`:** Essential for when you transition from dictionary-based in-memory data to database objects (9:01).
- **Status Codes:** Use `201 Created` for POST requests to follow RESTful best practices (13:42).
- **Error Handling:** *FastAPI* automatically returns a `422 Unprocessable Entity` error with detailed messages if validation fails (14:14).

## Day 5

In this tutorial, Corey Schafer demonstrates how to integrate a SQLite database into a FastAPI application using SQLAlchemy. This replaces the previous in-memory storage, ensuring data persistence across server restarts (0:00-0:30).
Key Architectural Concepts

```
Database Models: Use SQLAlchemy classes to define the schema (how data is stored) (1:36).
Pydantic Schemas: Used to validate API requests and format responses (1:45).
Dependency Injection: FastAPI uses Depends to manage database sessions, ensuring each request gets a clean session and proper cleanup (8:11).
```

Setup and Configuration

```
Installation: Install SQLAlchemy using uv add sqlalchemy or pip install sqlalchemy (4:27).
Database Connection (database.py): Configures the connection engine and provides a session factory.
```

python
database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./blog.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
db = SessionLocal()
try:
yield db
finally:
db.close()
Defining Models

Models define the database structure, including relationships like the one-to-many relationship between Users and Posts (9:50).

python
models.py

class User(Base):
tablename = "users"
id = mapped_column(Integer, primary_key=True)
username = mapped_column(String, unique=True, nullable=False)
posts = relationship("Post", back_populates="author")

class Post(Base):
tablename = "posts"
id = mapped_column(Integer, primary_key=True)
user_id = mapped_column(ForeignKey("users.id"), index=True)
author = relationship("User", back_populates="posts")
Updating API Endpoints

Routes now use dependency injection to interact with the database, replacing manual list operations (30:05).

python
main.py

@app.post("/api/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
new_user = User(username=user.username, email=user.email)
db.add(new_user)
db.commit()
db.refresh(new_user)
return new_user

By following this structure, you create a scalable foundation that can easily migrate to PostgreSQL or MySQL in the future by simply updating the connection string (1:03).

## Day 6

**CRUD (Create, Read, Update, Delete)** operations for a *FastAPI* application. Here are the key technical implementations and explanations provided by the creator:

### 1. Update Operations (PUT vs. PATCH)

- **PUT (Full Update):** Used to replace a resource entirely. The client must provide all fields (4:58). The logic involves re-using the `PostCreate` schema, verifying the resource existence (6:04), and performing direct attribute assignments:
python
post.title = post_data.title
post.content = post_data.content
post.user_id = post_data.user_id
db.commit()
- **PATCH (Partial Update):** Used to update only specific fields (1:36).
    - **Schema Setup:** All fields are defined as `Optional` with a `default=None` (2:45).
    - **Dynamic Update Logic:** To avoid overwriting missing fields with `None`, use `.model_dump(exclude_unset=True)` (12:12). Iterate through the dictionary and use `setattr` to update the model (13:45):
    python
    update_data = post_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
    setattr(post, field, value)
    db.commit()

### 2. Deletion and Cascade Logic

- **Delete Method:** Implemented using the `DELETE` verb. It returns a `204 No Content` status code (16:27), meaning the operation succeeded but there is no body to return.
- **Cascade Deletion:** Configured in `models.py` (27:29) so that removing a user automatically triggers the deletion of all their posts:
python
posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")
    - `all` ensures operations propagate, and `delete-orphan` cleans up records if they are removed from the relationship (28:06).

### 3. Validation and Status Codes

- **Validation:** Before performing updates or deletes, the code checks if the resource exists and raises an `HTTPException(status_code=404)` if not found (6:04, 17:11).
- **Common Status Codes:**
    - **200 OK:** Successful `GET`, `PUT`, or `PATCH` (19:11).
    - **201 Created:** Successful `POST` (19:19).
    - **204 No Content:** Successful `DELETE` (19:28).
    - **400 Bad Request:** Used for logical validation failures like duplicate usernames (19:34).
    - **422 Unprocessable Entity:** Automatic *Pydantic* validation error for malformed requests (19:50).

### 4. User Profile Pictures

- By adding an `image_file` string field to the user schema, the app stores only the filename (21:23). The actual file path is computed dynamically via a property on the model, allowing for flexible image management (33:07).

# Day 10

## Key Setup and Dependencies

- Password Hashing: Uses Argon2 via pwdlib for modern, secure password storage . This is chosen over BCrypt for better resistance to GPU cracking attacks.
- JWT Management: Utilizes the PyJWT library for creating and verifying tokens .
- Configuration: Implements pydantic-settings to manage environment variables securely, preventing sensitive data exposure in logs or code .

## Backend Implementation

- Database Updates: Added a password_hash field to the user model , ensuring no plain-text passwords are ever saved.
- Schema Security: Introduced distinct UserPublic and UserPrivate response schemas to ensure sensitive fields like emails are not exposed in public-facing API responses.
- Auth Utilities: Created oauth2_scheme and helper functions for hashing, verifying passwords, and handling JWT encoding/decoding .
  Endpoints: Implemented:
  Registration
  Login (/api/users/token)
  A current user endpoint (/me) to validate sessions .

## Frontend and UI Integration

- Templates: Created register.html and login.html pages with client-side form validation .
- State Management: Developed an auth.js module to manage JWT tokens in localStorage and update the navbar UI dynamically based on the user's logged-in status.

-> Note: While the authentication infrastructure is now complete, the video specifies that authorization (protecting routes and checking ownership for editing/deleting posts) is the focus of the next tutorial .

# Day 12

## Environment Setup & Prerequisites

* Pillow Library: Essential for image processing (resizing, format conversion).
* Installation: pip install pillow or uv add pillow.
* Python Multipart: Required for handling file uploads; included by default with standard fastapi installations.

## II. Image Processing Utilities

* Utilities Module (image_utils.py): Created to keep routing logic clean.
* Core Libraries: uuid (unique filenames), pathlib (modern file path handling), Pillow (Image, ImageOps).
* Orientation: Uses ImageOps.exif_transpose to prevent sideways images from phone uploads.
* Resizing: Uses Image.fit (300x300) with LANCZOS resampling.
* Format: Converts to RGB to handle transparency incompatibility with JPEGs, then saves as JPEG (quality 85, optimized).
* Security: Ignores user-provided filenames; generates unique IDs with uuid.uuid4().
* Deletion Logic: Helper function uses path.unlink to safely remove old images from the file system when a user updates their photo or deletes their account.

## III. Configuration & Validation

File Size Limit: Added max_upload_size to config.py (default 5MB) using Pydantic settings to prevent server overload.

## IV. Backend Implementation (users.router.py)

* Upload Endpoint: Uses UploadFile for multipart/form-data.
* Validation: Reads file bytes to verify size and uses Pillow to catch UnidentifiedImageError, which is more secure than trusting client-provided MIME types.
* Asynchronous Handling: Image processing is CPU-bound and blocks the event loop. The code uses starlet.concurrency.run_in_threadpool to execute processing off the main async thread.
* Safe Operations: Order of operations is critical: 1. Save new file, 2. Update database, 3. Delete old file. This prevents losing profile pictures if the database transaction fails.
* Security Update: Removed image_file from UserUpdate schema to prevent malicious users from bypassing upload validation by manually updating their profile URL.

## V. Front-end Integration

* Template: Updated account.html to include a preview container (initially hidden) and an accept="image/*" file input.
* JavaScript: Uses FileReader API for real-time image preview. Uses FormData to send the file; Do not manually set the Content-Type header (the browser must set this automatically to include the boundary string).
