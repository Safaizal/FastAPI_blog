from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

posts: list[dict] = [
        {
            "id": 1,
            "author": "faizal",
            "title": "Fastapi Framework",
            "content": "This is an opensourced easy framework",
            "date_posted": "september 2, 2025"
            },
        {
            "id": 2,
            "author": "faizal",
            "title": "Fastapi Framework",
            "content": "This is an opensourced easy framework",
            "date_posted": "september 2, 2025"
            }
        ]

#To give route we use decorators like in flask
@app.get("/", response_class=HTMLResponse, include_in_schema=False)
@app.get("/posts", response_class=HTMLResponse, include_in_schema=False)
def home():
    return f"<h1>{posts[0]['title']}</h1>"

@app.get("/api/posts")
def get_posts():
    return posts

