from flask_restful import Resource
from models import Book, Category, Barrow
from app import db

class BooksRequestHandler(Resource):
    def get(self, id):
        return {'Hello' : f'world {id}'}
    
    def delete(self, id):
        book = Book.query.get_or_404(id)

        db.session.delete(book)
        db.session.commit()

        return {'status' : 'success'}, 200

class CategoryRequestHandler(Resource):
    def delete(self, id):
        category = Category.query.get_or_404(id)
        db.session.delete(category)
        db.session.commit()

        return {'status' : 'success'}, 200
    
class BorrowBookRequestHandler(Resource):
    def delete(self, id):
        barrow = Barrow.query.get_or_404(id)
        db.session.delete(barrow)
        db.session.commit()

        return {'status' : 'success'}, 200
        