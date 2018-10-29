from flask import Flask, request, redirect, render_template
import cgi
import os

app = Flask(__name__)
app.config['DEBUG'] = True      

@app.route("/")
def index():
    return render_template('form.html')

def improper_length(value):
    if len(value) > 20 or len(value) < 3:
        return True

def not_empty(value):
    if value != "":
        return True

def find_char(char,value):
    char_exists = False

    for v in value:
        if v == char:
            char_exists = True

    return char_exists

@app.route("/", methods=["POST"])
def validate():
    username = request.form['username']
    password = request.form['password']
    confirm = request.form['confirm']
    email = request.form['email']

    username_error = ''
    password_error = ''
    confirm_error = ''
    email_error = ''

    if improper_length(username):
        username_error = "Username should be at least 3 characters and no more than 20 characters."

    if find_char(" ", username):
        username_error = "Username should not contain any spaces."

    if improper_length(password):
        password_error = "Password should be at least 3 characters and no more than 20 characters."

    if find_char(" ", password):
        password_error = "Password should not contain any spaces."
    
    if improper_length(confirm):
        confirm_error = "Password should be at least 3 characters and no more than 20 characters."

    if username is confirm:
        confirm_error = "Passwords must match."

    if not_empty(email):
        if improper_length(email):
            email_error = "Email should be at least 3 characters and no more than 20 characters."

        if find_char('@', email) == False:
            email_error = "That is not a valid email."

        if find_char('.', email) == False:
            email_error = "That is not a valid email."

    if not username_error and not password_error and not confirm_error and not email_error:
        return redirect('/success?username={0}'.format(username))
    else:
        return render_template('form.html', username=username, username_error=username_error, 
            password_error=password_error, confirm_error=confirm_error, email=email, email_error=email_error)

@app.route('/success')
def successful_login():
    username = request.args.get('username')
    return render_template('welcome.html', username=username)

app.run()