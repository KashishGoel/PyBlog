from flask import session

from src.common.database import Database
import uuid

from src.models.blog import Blog
from src.models.post import Post

class User:

    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    @classmethod
    def get_by_email(cls, email):
         data = Database.find_one('users', {'email': email})
         if data is not None:
            return cls(**data)

    @classmethod
    def get_by_id(cls, _id):
        data = Database.find_one('users', {'_id': _id})
        if data is not None:
            return cls(**data)

    @staticmethod
    def login_valid(email, password):
        user = User.get_by_email(email)
        if user is not None:
            return user.password == password
        return False

    @staticmethod
    def register(email,password):
        user = User.get_by_email(email)

        if user is None:
            user = User(email,password)
            user.save_to_mongo()
            session['email'] = email
            return True
        else:
            return False
    @staticmethod
    def login(user_email):
        session['email'] = user_email

    @staticmethod
    def logout():
        session['email'] = None

    def get_blogs(self):
        return Blog.find_by_author(author_id=self._id)

    def json(self):
        return {
            "email": self.email,
            "_id": self._id,
            "password": self.password
        }

    def save_to_mongo(self):
        Database.insert("users", self.json())

    def new_blog(self,title,description):
        blog = Blog(self.email, title, description, self._id)
        blog.save_to_mongo()

    def new_post(self, blog_id, title, content):
        blog = Blog.get_from_mongo(blog_id)
        blog.new_post(title, content)