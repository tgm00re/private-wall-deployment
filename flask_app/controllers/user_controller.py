import email
from flask_app import app
from flask import session, request, redirect, render_template, flash
from flask_bcrypt import Bcrypt
from flask_app.models import user, message

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/register_user', methods=['POST'])
def register_user():
    if not user.User.validate_user(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash
    }
    if user.User.get_by_email(data):
        flash("email already exists", 'register')
        return redirect('/')
    user.User.save(data)
    return redirect('/')

@app.route('/login_user', methods=['POST'])
def login_user():
    data = { "email": request.form['email'] }
    user_in_db = user.User.get_by_email(data)
    if not user_in_db:
        flash("Incorrect email/password", 'login')
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password[0], request.form['password']):
        flash("Incorrect email/password", 'login')
        return redirect('/')
    session['user_id'] = user_in_db.id
    session['first_name'] = user_in_db.first_name
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    data = {
        "id": session['user_id']
    }
    #message, sender_first, created_at
    dashboard_info = user.User.get_associated_messages(data)
    otherUsers = user.User.get_all_but_self(data)
    totalMessages = user.User.get_total_received(data)
    print("Printing dashboard info")
    print(dashboard_info[0])
    return render_template("dashboard.html", dashboard_info=dashboard_info, totalMessages=totalMessages, otherUsers=otherUsers)

@app.route('/delete_message/<int:id>')
def delete_message(id):
    #check if session['user_id'] is the same as the recipient of the message.
    data = {
        "id": id
    }
    print("Printing session")
    print(session['user_id'][0])
    message_recipient_id = message.Message.get_recipient_id(data)
    if(session['user_id'][0] != message_recipient_id):
        return redirect('/danger')
    message.Message.delete(data)
    return redirect('/dashboard')

@app.route('/create_message', methods=['POST'])
def create_message():
    data = {
        "message": request.form['message'],
        "recipient_id": request.form["recipient_id"],
        "sender_id": session['user_id'][0]
    }
    message.Message.save(data)
    return redirect('/dashboard')

@app.route('/danger')
def danger():
    return render_template("Danger.html")

@app.route('/clear_session')
def clear_session():
    session.clear()
    return redirect('/')
