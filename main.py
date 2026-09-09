from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
# it tells where to find the html pages
templates = Jinja2Templates(directory="templates")
#this is to tell to find css styles
app.mount("/static", StaticFiles(directory="static"), name="static")

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
            "title": "Fastapi2 Framework",
            "content": "This is an opensourced easy framework",
            "date_posted": "september 2, 2025"
            }
        ]

#To give route we use decorators like in flask
@app.get("/", include_in_schema=False, name="home")
@app.get("/posts", include_in_schema=False, name="posts")
def home(request: Request):
    return templates.TemplateResponse(request, "home.html", {"posts": posts, "title": "Home"})

@app.get("/api/posts")
def get_posts():
    return posts

