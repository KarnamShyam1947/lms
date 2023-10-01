from app import mail, app
from models import *
from datetime import timedelta, date
from flask import render_template
from flask_mail import Message

def send_reminder_mail(user, book, time, due_time):
    msg = Message('Gentle reminder to return book', recipients=[user.email, ], sender='vitap.library@gmail.com')

    context = {
        'user' : user,
        'book' : book,
        'time' : time,
        'due_date' : due_time
    }
    msg.body = ''
    msg.html = render_template('email/book_due_reminder.html', **context)

    mail.send(msg)

    print(f'reminder mail send to {user} ')

def send_late_submission_mail(user, book, time, due_time):
    msg = Message('Due expired on your book', recipients=[user.email, ], sender='vitap.library@gmail.com')

    context = {
        'user' : user,
        'book' : book,
        'time' : time,
        'due_date' : due_time
    }
    msg.body = ''
    msg.html = render_template('email/book_late_submission.html', **context)

    mail.send(msg)

    print(f'late submission mail send to {user} ')

def due_reminder():
    due_list = list()
    late_list = list()
    barrow_data = Barrow.query.all()

    for barrow_book in barrow_data:
        due_date = barrow_book.time + timedelta(days=1) # replace 6 (day before)

        if due_date.date() == date.today():
            # print(barrow_book.user_id, due_date.date())
            due_list.append((barrow_book.user_id, barrow_book.book_id, barrow_book.time))

    for barrow_book in barrow_data:
        late_date = barrow_book.time + timedelta(days=3) # replace 8 (next date)
           
        if late_date.date() == date.today():
            # print(barrow_book.user_id, late_date.date())
            late_list.append((barrow_book.user_id, barrow_book.book_id, barrow_book.time))

    for uid, bid, barrow_time in due_list:
        with app.app_context():
            user = User.query.filter_by(id = uid).first()
            book = Book.query.filter_by(id = bid).first()
            due_time = barrow_time + timedelta(days=2) # replace 7 (actual date)

            send_reminder_mail(user, book, barrow_time, due_time)
    
    for uid, bid, barrow_time in late_list:
        with app.app_context():
            user = User.query.filter_by(id = uid).first()
            book = Book.query.filter_by(id = bid).first()
            due_time = barrow_time + timedelta(days=2) # replace 7 (actual date)

            send_late_submission_mail(user, book, barrow_time, due_time)

if __name__ == '__main__':
    due_reminder()

