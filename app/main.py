from email import message
from operator import index
from os import stat
from turtle import pos
from typing import Optional
from fastapi import FastAPI, Response,  status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

# request Get method url: "/"

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int]= None
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

my_posts = [{"title": "title of post 1",
            "content": "content of post 1",
            "id": 1,},
            {"title": "favorite foods",
            "content": "I like pizza",
            "id": 2}]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p ['id'] ==  id:
            return i

@app.get("/")
def read_root():
    return {"Heyy": "welcome to my API"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)   
def create_posts(post: Post):
    cursor.execute("""INSERT INTO posts(title, content, published) VALUES(%s, %s, %s) RETURNING *""",(post.title, 
    post.content, post.published))

    new_post = cursor.fetchone()

    conn.commit()

    return{"data": new_post}
    # print(post)
    # print(post.dict())
    # post_dict = post.dict()
    # post_dict['id'] = randrange(0, 100000)
    # my_posts.append(post_dict)

    
# title str, content str,

# @app.get("/posts/latest")
# def get_latest_post():
#     post = my_posts[len(my_posts)-1]
#     return {"detail": post}

@app.get("/posts/{id}")
def get_post(id: int):
    # print(type(id))
    post = find_post(id)
    # return{"post_detail": f"here is post {id}"}
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id {id} was not found"}
    return{"post_detail": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    #deleting post
    # find the index in the array that has the required ID
    # my_post.pop(index)
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: ({id}) does not exist")

    my_posts.pop(index)
    # return{"message": 'post was successfully deleted'}
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return{"data": post_dict}
    print(post)
    return{"message": "updated post"}