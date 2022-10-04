

from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List

from app import oauth2
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix= "/posts",
    tags=["Posts"] 
)


@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)   
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts(title, content, published) VALUES(%s, %s, %s) RETURNING *""",(post.title, 
    # post.content, post.published))

    # new_post = cursor.fetchone()

    # conn.commit()
    # print(**post.dict())
    print(current_user.email)
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
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

@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    # post = cursor.fetchone()
    # return{"post_detail": f"here is post {id}"}
    post = db.query(models.Post).filter(models.Post.id == id).first()
    # print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id {id} was not found"}
    return post

@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING*""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: ({id}) does not exist")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    # return {"Response": f"successfully deleted post with id: {id}"}

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,(post.title, post.content, post.published, str(id)))

    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exit")
    post_query.update({'title': 'hey this is my updated title', 'content': 'this is my updated content'}, synchronize_session=False)

    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return post_query.first()

