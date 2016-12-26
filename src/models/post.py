from src.common.database import Database
import uuid
import datetime
class Post():
    def __init__(self, blogID, title, content, author, created_date=datetime.datetime.utcnow(), _id=None):
        self.title = title
        self.author = author
        self.content = content
        self.blog_id = blogID
        self._id = uuid.uuid4().hex if _id is None else _id
        self.created_date = created_datedate

    def save(self):
        Database.insert(collection='post', data=self.json())

    def json(self):
        return {
            'title':self.title,
            'author':self.author,
            'content': self.content,
            'blog_id':self.blog_id,
            '_id': self._id,
            'created_date': self.created_date

        }


    @staticmethod
    def from_mongo(cls,id):
        data = Database.find_one(collection='post', query={'_id': id})
        return cls(**data)
    @staticmethod
    def from_blog(id):
        return [post for post in Database.find(collection='post', query={'blog_id': id})]
