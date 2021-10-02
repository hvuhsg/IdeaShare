from os import getenv
from dotenv import load_dotenv
from datetime import datetime
from qwhale_client import APIClient


load_dotenv(".env")
TOKEN = getenv("QWHALE_TOKEN")
if TOKEN is None:
    raise RuntimeError(".env file with QWHALE_TOKEN is required")


class DB:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.__client = APIClient(TOKEN)
        self.__db = self.__client.get_database()
        self.__ideas = self.__db.get_collection("ideas")
        self.__searches = self.__db.get_collection("searches")

    def create_idea(self, idea_dict: dict):
        self.__ideas.insert_one(idea_dict)

    def search_ideas(self, query: str):
        def remove_score(doc: dict):
            del doc["score"]
            del doc["search_score"]
            return doc
        return list(
            map(
                remove_score,
                self.__ideas.find(
                    {"$text": {"$search": query}},
                    {"search_score": {"$meta": "textScore"}, "_id": 0}
                ).sort([("search_score", -1), ("score", -1)]))
        )

    def upvote_idea(self, idea_id: str, cancel: bool = False):
        increment = -1 if cancel else 1
        self.__ideas.update_one({"id": idea_id}, {"$inc": {"upvote": increment, "score": increment}})

    def downvote_idea(self, idea_id: str, cancel: bool = False):
        increment = -1 if cancel else 1
        self.__ideas.update_one({"id": idea_id}, {"$inc": {"downvote": increment, "score": -increment}})

    def save_search(self, search_query: str):
        self.__searches.insert_one({"searched_at": datetime.now(), "query": search_query})

    def close(self):
        self.__client.close()
