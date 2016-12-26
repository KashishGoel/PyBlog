
import uuid
import datetime
from src.common.database import Database
from src.models.post import Post

class Blog:

    def __init__(self, author, title, description, author_id, _id=None):

        self.author = author
        self.title = title
        self.description = description
        self.author_id = author_id
        self._id = uuid.uuid4().hex if _id is None else _id



    def new_post(self,title,content,date=datetime.datetime.utcnow()):
        post = Post(blogID=self._id,
                    title=title,
                    content=content,
                    author=self.author,
                    date=date

                    )
        post.save()

    def get_post(self):
        return Post.from_blog(self._id)


    def save_to_mongo(self):
        Database.insert(collection='blogs', data=self.json())

    def json(self):
        return{
            "author":self.author,
            "title":self.title,
            "description":self.description,
            "author_id":self.author_id,
            "_id":self._id
        }

    def get_from_mongo(_id):
        blog_data = Database.find_one(collection="blogs", query={"_id": _id})
        return Blog(author=blog_data['author'],
                    title=blog_data['title'],
                    description=blog_data['description'],
                    id=blog_data['_id'])

    @classmethod
    def find_by_author(cls,author_id):
        blogs = Database.find("blogs",({"author_id":author_id}))
        return [cls(**blog) for blog in blogs]