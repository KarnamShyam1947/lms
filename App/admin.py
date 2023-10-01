from flask import Blueprint, render_template, request, flash, redirect, url_for, abort
from werkzeug.utils import secure_filename
from flask_login import current_user
from models import *
from defalut_img import default_image
import base64

admin = Blueprint('admin', __name__)

@admin.route('/admin')
def home():
    if not current_user.is_authenticated:
        abort(403)
    
    if current_user.isAdmin != 1:
        abort(403)
    
    books = Book.query.all()
    category_obj = Category()
    user_obj = User()
    book_obj = Book()

    page = request.args.get("page")

    if page and page.isdigit():
        page = int(page)

    else:
        page = 1

    pages = Book.query.paginate(page=page, per_page=3)

    context = {
        "books" : books,
        "pages" : pages,
        'c' : category_obj,
        'b' : book_obj,
        'u' : user_obj
    }

    return render_template('admin/home.html', **context)

@admin.route('/add-book',methods=['GET', 'POST'])
def add_book():
    if not current_user.is_authenticated:
        abort(403)
    
    if current_user.isAdmin != 1:
        abort(403)
       
    if request.method == 'POST':
        book_name = request.form.get('book_name')
        author = request.form.get('author')
        price = request.form.get('price')
        book_info = request.form.get('book_info')
        edition = request.form.get('edition')
        language = request.form.get('language')
        length = request.form.get('length')
        publisher = request.form.get('publisher')
        category = request.form.get('category')
        image = request.files["file"]

        print(category)

        if image:
            image_url = image.read()

            image_url = base64.b64encode(image_url)
            image_url = str(image_url, 'utf-8')
            
        else:
            image_url = default_image

        

        book = Book.query.filter_by(name =book_name).first()
        if book:
            flash("Error : Book already exists with same title", "error")
            return redirect(url_for("admin.add_book"))
        
        else:
            new_book = Book(name=book_name, author=author, price=price, length=length,
                            book_info=book_info, edition=edition, language=language,
                            publisher=publisher, category_id = category, image_url=image_url)
            
            db.session.add(new_book)
            db.session.commit()

            flash("Book added successfully", "success")
            return redirect(url_for("admin.home"))
    
    categories = Category.query.all()
    category_obj = Category()
    user_obj = User()
    book_obj = Book()

    context = {
        "categories" : categories,
        'c' : category_obj,
        'b' : book_obj,
        'u' : user_obj
    }
    return render_template('admin/add_book.html', **context)

@admin.route('/update-book/<book_id>',methods=['GET', 'POST'])
def update_book(book_id):
    book = Book.query.get(book_id)

    if not current_user.is_authenticated:
        abort(403)
    
    if current_user.isAdmin != 1:
        abort(403)
       
    if request.method == 'POST':
        book_name = request.form.get('book_name')
        author = request.form.get('author')
        price = request.form.get('price')
        book_info = request.form.get('book_info')
        edition = request.form.get('edition')
        language = request.form.get('language')
        length = request.form.get('length')
        publisher = request.form.get('publisher')
        # category_name = request.form.get('category')
        # print(category_name)
        image = request.files["file"]

        if image:
            file_name = book.image_url[1:]
            image.save(file_name)

        book.author = author
        book.length = length
        book.price = price
        book.edition = edition
        book.language = language
        book.book_info = book_info
        book.publisher = publisher
        # book.category = Category.query.filter_by(category_name=category_name).first()
        # print(Category.query.filter_by(category_name=category_name).first())
        
        # db.session.add(book)
        db.session.commit()

        flash("Book updated successfully", "success")
        return redirect(url_for("admin.home"))
    
    categories = Category.query.all()
    category_obj = Category()
    book_obj = Book()
    user_obj = User()

    context = {
        "categories" : categories,
        'book' : book,
        'c' : category_obj,
        'b' : book_obj,
        'u' : user_obj,
    }
    return render_template('admin/update_book.html', **context)

@admin.route('/category')
def category():
    if not current_user.is_authenticated:
        abort(403)
    
    if current_user.isAdmin != 1:
        abort(403) 

    categories = Category.query.all()
    c = Category()
    u = User()
    b = Book()
    data = c.get_category_info()

    context = {
        "categories" : categories,
        "data": data,
        'c' : c,
        'b' : b,
        'u' : u
    }

    return render_template('admin/category.html', **context)

@admin.route('/add-category', methods = ['GET', 'POST'])
def add_category():
    if not current_user.is_authenticated:
        abort(403)
    
    if current_user.isAdmin != 1:
        abort(403)
    
    if request.method == 'POST':
        category_name = request.form.get('category_name')
        category_info = request.form.get('category_info')

        category = Category.query.filter_by(category_name=category_name).first()
        if category:
            flash("Category already exists", "error")
            return redirect(url_for('admin.add_category'))
        
        else:
            new_category = Category(category_name = category_name, category_info = category_info)
            db.session.add(new_category)
            db.session.commit()

            flash("New category added successfully", "success")
            return redirect(url_for("admin.category"))
        
    category_obj = Category()
    user_obj = User()
    book_obj = Book()

    context = {
        'c' : category_obj,
        'b' : book_obj,
        'u' : user_obj
    }
    return render_template('admin/add_category.html', **context)

@admin.route('/users')
def users():
    if not current_user.is_authenticated:
        abort(403)
    
    if current_user.isAdmin != 1:
        abort(403)
    

    category_obj = Category()
    user_obj = User()
    book_obj = Book()
    users_data = User.query.all()

    context = {
        'users' : users_data,
        'c' : category_obj,
        'b' : book_obj,
        'u' : user_obj
    }
    return render_template('admin/users.html', **context)
