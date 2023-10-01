from app import db
from flask_login import UserMixin, current_user
from datetime import datetime, timedelta

class Category(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    category_name = db.Column(db.String(50), unique=True)
    category_info = db.Column(db.String(300))
    books = db.relationship("Book", backref = 'category', cascade='all, delete')

    def __repr__(self):
        return self.category_name
    
    def get_count(self):
        return len(Category.query.all())
    
    def get_category_info(self):
        cs = db.session.query(Category.category_name, Category.category_info, Book.category_id, db.func.count(Book.id)).outerjoin(Book, Book.category_id == Category.id).all()
        c = Category.query.all()
        result = list()

        for r in c:
            for rs in cs:
                    if r.id == rs[1]:
                        result.append((r.id, r.category_name, r.category_info, rs[3]))
                        continue
                    else:
                        result.append((r.id, r.category_name, r.category_info, 0))

        return result

class Book(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(50))
    author = db.Column(db.String(50))
    price = db.Column(db.Integer)
    book_info = db.Column(db.Text)
    length = db.Column(db.Integer)
    image_url = db.Column(db.Text)
    edition = db.Column(db.String(30))
    language = db.Column(db.String(30))
    publisher = db.Column(db.String(100))
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))

    def __repr__(self):
        return self.name
    
    def get_count(self):
        return len(Book.query.all())
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(255))
    isAdmin = db.Column(db.Integer, default = 0)
    isVerified = db.Column(db.Integer, default = 0)
    books = db.relationship("Barrow", backref = 'user', cascade='all, delete')

    def __repr__(self):
        return self.name
    
    def get_count(self):
        return len(User.query.all())
    
class Barrow(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    time = db.Column(db.DateTime, default=datetime.now)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'book_id'),
    )

    def __repr__(self):
        return f'U{self.user_id} - B{self.book_id}'
    
    
    def get_count(self):
        books = db.session.query(
            Book.id,
            Book.name,
            Book.author,
            Barrow.time,
            Barrow.id.label('barrow_id')
        ).join(Barrow, Barrow.book_id == Book.id).filter(Barrow.user_id == current_user.id).all()

        return len(books)

