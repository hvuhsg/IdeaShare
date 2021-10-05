from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware

from models import Idea
from db import DB

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    DB.get_instance()


@app.on_event("shutdown")
def shutdown():
    DB.get_instance().close()


@app.put("/idea", status_code=201)
def create_idea(name: str = Form(default=None, max_length=50), tldr: str = Form(default=None, max_length=400)):
    db = DB.get_instance()
    full_idea = Idea(**{"name": name, "tldr": tldr})
    db.create_idea(full_idea.dict())
    return {"created": full_idea.id}


@app.get("/search")
def search_ideas(q: str):
    db = DB.get_instance()
    if not q:
        return db.main_page_ideas()
    results = db.search_ideas(q)
    db.save_search(q)
    return results


@app.post("/upvote")
def upvote(idea_id: str, cancel: bool = False):
    db = DB.get_instance()
    db.upvote_idea(idea_id, cancel)


@app.post("/downvote")
def downvote(idea_id: str, cancel: bool = False):
    db = DB.get_instance()
    db.downvote_idea(idea_id, cancel)
