from fastapi import FastAPI

from models import NewIdea, Idea
from db import DB

app = FastAPI()


@app.on_event("startup")
def startup():
    DB.get_instance()


@app.on_event("shutdown")
def shutdown():
    DB.get_instance().close()


@app.put("/idea", status_code=201)
def create_idea(idea: NewIdea):
    db = DB.get_instance()
    full_idea = Idea(**idea.dict())
    db.create_idea(full_idea.dict())
    return {"created": full_idea.id}


@app.get("/search")
def search_ideas(q: str):
    db = DB.get_instance()
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
