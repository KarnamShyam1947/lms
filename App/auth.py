from flask import Blueprint, render_template, redirect, request, url_for, flash, session
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from flask_login import login_user, logout_user, login_required, current_user
from app import bcrypt, db, mail, app
from flask_mail import  Message
from models import *
import threading

auth = Blueprint('auth', __name__)

tokenizer = URLSafeTimedSerializer('this-is-secret')

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember') 
        next_page = request.form.get('next_page') 

        if remember is None:
            r = False
        else:
            r = True
        
        user = User.query.filter_by(email = email).first()

        if user is None :
            flash("invalid email or password", "error")
            return redirect(url_for('auth.login'))
        
        hashed_password = user.password
        if not bcrypt.check_password_hash(hashed_password, password):
            flash("invalid email or password", "error")
            return redirect(url_for('auth.login'))
        
        if user.isVerified == 0:
            token = tokenizer.dumps(email)
            link = url_for('auth.activate', token=token, _external=True)

            print(link)
            threading.Thread(target=send_activation_mail, args=(user, link, )).start()
            flash(f"Your email is not verified. Please check your inbox", "error")
            return redirect(url_for('auth.login'))
        
        else:
            login_user(user, r)
            if next_page:
                return redirect(next_page)
            
            return redirect(url_for('main.index'))

    next_page = request.args.get('next', None)
    print(next_page)

    return render_template('auth/login.html', next_page = next_page)

@auth.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password1 = request.form.get('password1')

        if password != password1:
            flash("Error : passwords didn't match", 'error')
            return redirect(url_for('auth.register'))
        
        user = User.query.filter_by(email = email).first()
        if user is not None:
            flash("Error : email already in use", 'error')
            return redirect(url_for('auth.register'))
        
        new_user = User(name = username, email = email, password = bcrypt.generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully. Don't forgot to activation it", "success")
        return redirect(url_for('auth.login'))

    
    return render_template('auth/register.html')

@auth.route('/activate/<token>')
def activate(token):
    try:
        email = tokenizer.loads(token, 3600)

        user = User.query.filter_by(email = email).first()

        if user is None :
            flash("invalid token", "error")
            return redirect(url_for('auth.login')) 
        
        else:
            user.isVerified = 1
            db.session.add(user)
            db.session.commit()

            flash("verified successfully", "success")
            return redirect(url_for('auth.login'))
        
    except SignatureExpired:
        flash("Link expired", "error")
        return redirect(url_for('auth.login')) 
    
    except BadSignature:
        flash("Invalid link", "error")
        return redirect(url_for('auth.login')) 

@auth.route('/logout')
def logout():
    logout_user()

    return redirect(url_for('main.index'))

@auth.route('/forgot-password', methods = ['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')

        user = User.query.filter_by(email = email).first()

        if user is None:
            flash("Email not registered.....!!!", "error")
            return redirect(url_for('auth.forgot_password'))
        
        else:
            token = tokenizer.dumps(email)
            link = url_for('auth.validate_token', token=token, _external=True)
            # print(f"\n{link}\n")

            threading.Thread(target=send_password_reset_mail, args=(user, link, )).start()

            flash("Check your inbox for password reset link", "error")
            return redirect(url_for('auth.forgot_password'))

    return render_template('auth/forgot-password.html')

@auth.route('/validate-token/<token>')
def validate_token(token):
    try:
        email = tokenizer.loads(token, 3600)

        user = User.query.filter_by(email = email).first()

        if user is None :
            flash("invalid url", "error")
            return redirect(url_for('auth.login')) 
        
        else:
            session['forgot_password_email'] = email
            return redirect(url_for('auth.set_password'))
        
    except SignatureExpired:
        flash("Link expired", "error")
        return redirect(url_for('auth.login')) 
    
    except BadSignature:
        flash("Invalid link", "error")
        return redirect(url_for('auth.login')) 

@auth.route('/set-password', methods = ['GET', 'POST'])
def set_password():
    if 'forgot_password_email' not in session:
        flash("403 : forbidden", "error")
        return redirect(url_for('auth.login'))
    
    else:
        if request.method == 'POST':
            password1 = request.form.get("password1")
            password2 = request.form.get("password2")

            if password1 != password2:
                flash("passwords didn\'t match", "error")
                return render_template('auth/set-password.html')
            
            else:
                email = session['forgot_password_email']
                user = User.query.filter_by(email = email).first()

                user.password = bcrypt.generate_password_hash(password1)

                db.session.add(user)
                db.session.commit()

                flash("password changed successfully.....!!!", "success")

                session.pop('forgot_password_email', None)

                return redirect(url_for("auth.login"))

        return render_template('auth/set-password.html')

@auth.route('/change-password', methods = ['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        old_password = request.form.get("old_password")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        current_password = current_user.password
        if not bcrypt.check_password_hash(current_password, old_password):
            flash("Old password doesn\'t match.....!!!", "error")
            return redirect(url_for("auth.change_password"))
        
        if password1 != password2:
            flash("conform password doesn\'t match", "error")
            return redirect(url_for("auth.change_password"))
        
        else:
            current_user.password = bcrypt.generate_password_hash(password1)

            db.session.add(current_user)
            db.session.commit()

            flash("Password changed successfully", "success")
            return redirect(url_for("auth.change_password"))

    return render_template('auth/change-password.html')

def send_activation_mail(user, link):
    with app.app_context():
        print('started..........')
        msg = Message('Activate your account', recipients=[user.email, ], sender='ecsgps.project@gmail.com')

        msg.html = render_template('email/active.html', name=user.name, link=link)

        mail.send(msg)

        print("Send successfully.........")

def send_password_reset_mail(user, link):
    with app.app_context():
        print('started..........')
        msg = Message('Password Reset link', recipients=[user.email, ], sender='ecsgps.project@gmail.com')

        msg.html = render_template('email/forget-password.html', name=user.name, link=link)

        mail.send(msg)

        print("Send successfully.........")
