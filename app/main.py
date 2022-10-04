from email import message
from msilib import schema
from multiprocessing import synchronize
from operator import index
from os import stat
from turtle import pos
from typing import Optional, List
from fastapi import FastAPI, Response,  status, HTTPException, Depends
from fastapi.params import Body
from importlib_metadata import Deprecated

from pydantic import BaseModel

from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

from . import models, schemas, utils
from .database import engine, get_db

from .routers import post, user, auth


models.Base.metadata.create_all(bind=engine)

app = FastAPI()



# request Get method url: "/"


    # rating: Optional[int]= None
while True:

    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='taiye1692', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("Connecting to Database failed")
        print("Error", error)
        time.sleep(2)

# my_posts = [{"title": "title of post 1",
#             "content": "content of post 1",
#             "id": 1,},
#             {"title": "favorite foods",
#             "content": "I like pizza",
#             "id": 2}]

# def find_post(id):
#     for p in my_posts:
#         if p['id'] == id:
#             return p

# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p ['id'] ==  id:
#             return i

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"Heyy": "welcome to my API"}

# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):

#     posts = db.query(models.Post).all()
#     return{"data": posts}


