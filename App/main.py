from flask import Blueprint, render_template, request
from flask_login import current_user
from models import *

main = Blueprint('main', __name__)

@main.route('/')
def index():
    books = Book.query.all()
    flag = False

    if len(books) > 4:
        books = books[-4:]
        flag = True

    return render_template('index.html', books = books, flag=flag)


@main.route('/store', methods=['GET', 'POST'])
def store():
    books = Book.query.all()
    categories = Category.query.all()

    if request.method == 'POST':
        search_text = request.form.get('keyword')
        search_category = request.form.get('category')
        search_str = ''
        category_name = ''

        if search_category != '0':
            category_name = Category.query.filter_by(id = search_category).first().category_name

        if search_text.strip() != '' and search_category != '0': # word with category
            books = Book.query.filter_by(category_id=search_category). \
                    filter(Book.name.like('%' + search_text  +'%')).all()
            
            bs = Book.query.filter_by(category_id=search_category). \
                    filter(Book.author.like('%' + search_text  +'%')).all()
            
            books.extend(bs)
            books = list(set(books))

            search_str = f'{search_text} in Category {category_name}'
            
        elif search_text.strip() != '': # only word
            books = Book.query.filter(Book.name.like('%' + search_text  +'%')).all()
            bs = Book.query.filter(Book.author.like('%' + search_text  +'%')).all()
            books.extend(bs)
            books = list(set(books))
            search_str = search_text

            # return render_template('pages/store.html', books = books, categories=categories, search_str = search_str)

        else:
            books = Book.query.filter_by(category_id=search_category).all()
            search_str = f'Category {category_name}'

        return render_template('pages/store.html', books = books, categories=categories, search_str = search_str)
    
    return render_template('pages/store.html', books = books, categories=categories)

@main.route('/contact')
def contact():
    return render_template('pages/contact.html')

@main.route('/services')
def services():
    return render_template('pages/services.html')