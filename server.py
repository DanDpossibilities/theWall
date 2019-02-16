from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import connectToMySQL
app = Flask(__name__)
app.secret_key = 'super_secret'
from flask_bcrypt import Bcrypt
import re
from datetime import datetime
from datetime import timedelta
bcrypt = Bcrypt(app)    # we are creating an object called bcrypt, which is made by invoking the function Bcrypt with our app as an argument
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


#----------------Get routes-----------------#
@app.route('/')
def home():
    print(request.form)
    return render_template('home.html')

@app.route('/success/<id>')
def success(id):
    name = db_get_from_id(session['id'])
    session['name'] = name[0]['first_name']
    return render_template('success.html')

@app.route('/wall')
def messaging():
    name = db_get_from_id(session['id'])
    session['name'] = name[0]['first_name']
    current_user = {
        'reg_id': session['id']
    }
    current_messages = received_messages(current_user)
    count = len(current_messages)
    print('&'*87)
    users = users_to_message(current_user)
    print(users)
    return render_template('messages.html', users = users, current_messages = current_messages, count =  count, now = datetime.now())


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


#------------------Post routes -----------------------#
@app.route('/register', methods=['POST'])
def register():
    print(request.form)
    is_valid = True
    if len(request.form['first_name']) < 2 or not(request.form['first_name'].isalpha()):
        is_valid = False
        flash("Please enter a first name with letters only")
    if len(request.form['last_name']) < 2 or not(request.form['last_name'].isalpha()):
        is_valid = False
        flash("Please enter a last name with letters only")
    if not EMAIL_REGEX.match(request.form['email']):
        flash("Invalid email address!")
    if len(request.form['password']) < 8:
        is_valid = False
        flash('Password must be at least 8 characters long')
    if request.form['password'] != request.form['confirm']:
        is_valid = False
        flash('Password and confirm password must be the same')

    if not '_flashes' in session.keys():
        flash("Registration successfully added!")
        hashpass = bcrypt.generate_password_hash(request.form['password'])
        userInfo = {
            "first_name": request.form["first_name"],
            "last_name": request.form["last_name"],
            "email": request.form["email"],
            "pass": hashpass
        }

        new_registration_id = db_add_user(userInfo)
        session['id'] = new_registration_id
        return redirect(f"/success/{new_registration_id}")
    return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    print(request.form)
    is_valid = True
    if not EMAIL_REGEX.match(request.form['email']):
        flash("Invalid email address!")
    if len(request.form['password']) < 8:
        is_valid = False
        flash('Password must be at least 8 characters long')

    if not '_flashes' in session.keys():
        new_registration_id = db_get_from_email(request.form['email'])
        print('^'*90)
        print(new_registration_id)
        check = bcrypt.check_password_hash(new_registration_id[0]['password'], request.form['password'])
        print(new_registration_id[0])
        print(request.form)
        print(check)
        if check is True:
            pass
        else:
            flash('Please try again')
            return redirect('/')

        session['id'] = new_registration_id[0]['registration_id']
        flash("Login successful!")
        return redirect(f"/success/{session['id']}")
    return redirect('/')

@app.route('/delete', methods=['POST'])
def delete_message():
    print(request.form)
    print(session)
    message_to_delete = {
        'message_id': request.form['deleted_message']
    }
    deleting_message(message_to_delete)
    return redirect ('/wall')

@app.route('/send_message', methods=['POST'])
def send_message_now():
    print('#'*95)
    print(request.form)
    print(session)
    message = {
        'id': request.form['users_list'],
        'comment': request.form['comment'],
        'sender': session['id']
    }
    my_id = {
        'sender': session['id']
    }
    total_messages = count_my_messages(my_id)
    total_count = 1
    for x in range(len(total_messages)):
        total_count += 1

    flash('You have sent ' + str(total_count) + 'messages.')
    send_my_message(message)
    return redirect('/wall')

#-------------------- DATABASES ----------------------#
def db_add_user(userInfo):
    mysql = connectToMySQL("login_registration")

    query = "INSERT INTO registrations (first_name, last_name, email, password, created_at, updated_at) VALUES (%(fn)s, %(ln)s, %(e)s, %(pass)s, NOW(), NOW());"
    data = {
        "fn": userInfo["first_name"],
        "ln": userInfo["last_name"],
        "e": userInfo["email"],
        "pass": userInfo["pass"]
    }
    return mysql.query_db(query, data)

def db_get_from_id(uid):
    mysql = connectToMySQL("login_registration")
    query = "SELECT * FROM registrations WHERE registration_id = %(id)s;"
    data = {
        "id": uid
    }
    return mysql.query_db(query, data)

def db_get_from_email(email):
    mysql = connectToMySQL("login_registration")
    query = "SELECT * FROM registrations WHERE email = %(e)s;"
    data = {
        "e": email,
    }
    return mysql.query_db(query, data)

def users_to_message(current_user):
    mysql = connectToMySQL('login_registration')
    query = 'SELECT registration_id, registrations.first_name, registrations.last_name FROM registrations WHERE registration_id != %(reg_id)s ORDER BY first_name ASC;'
    data = {
        'reg_id': current_user['reg_id'],
    }
    return mysql.query_db(query, data)

def received_messages(current_user):
    mysql = connectToMySQL('login_registration')
    query = 'SELECT registrations.first_name, messages.message_id, messages.message_content, messages.created_at FROM messages JOIN registrations ON registrations.registration_id = messages.sender_id WHERE receiver_id = %(reg_id)s ORDER BY messages.created_at ASC;'
    data = {
        'reg_id': current_user['reg_id'],
    }
    return mysql.query_db(query, data)

def deleting_message(message_to_delete):
    mysql = connectToMySQL('login_registration')
    query = 'DELETE FROM messages WHERE messages.message_id = %(msg_id)s'
    data = {
        'msg_id': message_to_delete['message_id'],
    }
    return mysql.query_db(query, data)

def send_my_message(message):
    mysql = connectToMySQL('login_registration')
    query = "INSERT INTO messages (sender_id, message_content, receiver_id) VALUES (%(sender)s, %(comment)s, %(id)s);"
    data = {
        'id': message['id'],
        'comment': message['comment'],
        'sender': message['sender']
    }
    return mysql.query_db(query, data)

def count_my_messages(my_id):
    mysql = connectToMySQL('login_registration')
    query = "SELECT * FROM messages WHERE (sender_id = %(sender)s);"
    data = {
        'sender': my_id['sender']
    }
    return mysql.query_db(query, data)

if __name__ == "__main__":
    app.run(debug=True)