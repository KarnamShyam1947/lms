from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from flask_mail import Message
from app import db, mail
from models import *
import threading

book = Blueprint('book', __name__)

@book.route('/add-to-cart')
def add_to_cart():
    book_id = request.args.get('book-id')
    user_id = current_user.id

    b_check = Barrow.query.filter_by(user_id=user_id, book_id=book_id).first()

    if b_check:
        flash('You already taken this book','error')
        return redirect(url_for('book.book_cart'))
    
    book = Book.query.filter_by(id=book_id).first()
    barrow = Barrow(user_id=user_id, book_id=book_id)

    db.session.add(barrow)
    db.session.commit()
    
    due_date = barrow.time + timedelta(days=7)
    send_book_issue_mail(current_user, book, barrow, due_date)

    flash('Book borrowed successfully', 'success')

    return redirect(url_for('book.book_cart'))


@book.route('/cart')
@login_required
def book_cart():
    due_date = list()
    books = db.session.query(
        Book.id,
        Book.name,
        Book.author,
        Barrow.time,
        Barrow.id.label('barrow_id')
    ).join(Barrow, Barrow.book_id == Book.id).filter(Barrow.user_id == current_user.id).all()

    for book in books:
        due_date.append(book.time + timedelta(days=7))

    books = zip(books, due_date)

    return render_template('pages/cart.html', books=books)

def send_book_issue_mail(user, book, barrow, due_date):
    msg = Message('Library Check out details', recipients=[user.email, ], sender='vitap.library@gmail.com')
    msg.html = render_template('email/book_issue.html', user=user, book=book, barrow=barrow, due_date=due_date)
    msg.body = ''

    mail.send(msg)
