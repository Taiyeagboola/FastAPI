from cgitb import text
import email
from email.policy import default
from tkinter import CASCADE
from xmlrpc.client import Boolean
from sqlalchemy import Column, ForeignKey,Integer,String,Boolean
from .database import Base
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='True',nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)


class User(Base):
    __tablename__ ='users'

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    date_created = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))