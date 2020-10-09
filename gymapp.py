from flask import Flask, redirect, url_for, request, render_template
from passlib.hash import sha256_crypt
import pymysql

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/create_account')
def create_account():
    return render_template('account_form.html')


# @app.route('/account_complete',  methods=['POST'])
# def account_complete():
#     user = request.form['username']
#     pm = request.form['password']
#     email = request.form["email"]
#     with open('static/users.txt', 'a') as f:
#         password = sha256_crypt.encrypt(pm)
#         f.write(user+','+password+','+email)
#         f.write('\n')
#     return redirect(url_for('userpage', username=user))


@app.route('/account_complete',  methods=['POST'])
def account_complete():
    username = request.form['username']
    password = sha256_crypt.hash(request.form['password'])
    email = request.form["email"]
    print(password)

    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='password',
                                 db='userdata')
    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO userlogin (username, email, password) VALUES (%s, %s, %s);"
            cursor.execute(sql, (username, email, password))
        # Save changes
        connection.commit()
    finally:
        connection.close()

    return redirect(url_for('userpage', username=username))


@app.route('/u/<username>')
def userpage(username):
    return render_template('userpage.html', name=username)


@app.route('/login')
@app.route('/login/<err>')
def login(err='none'):
    print(err, type(err))
    return render_template('login.html', error=err)


# @app.route('/login/authentication', methods=['POST'])
# def login_auth():
#     user = request.form["username"]
#     pw = request.form["password"]
#     success = False
#     with open('static/users.txt', 'r') as f:
#         for line in f:
#             line = line.split(',')
#             if line[0] == user and sha256_crypt.verify(pw, line[1]):
#                 print("success")
#                 success = True
#                 break
#     if success:
#         return redirect(url_for('userpage', username=user))
#     else:
#         return redirect(url_for('login', err='failed'))

@app.route('/login/authentication', methods=['POST'])
def login_auth():
    username = request.form["username"]
    password = request.form["password"]
    success = False

    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='password',
                                 db='userdata')
    try:
        with connection.cursor() as cursor:
            # Fetch password hash
            sql = "SELECT password FROM userlogin WHERE username = %s;"
            cursor.execute(sql, username)
            pw_hash = cursor.fetchone()[0]
            # verify password
            if sha256_crypt.verify(password, pw_hash):
                success = True
    finally:
        connection.close()

        # for line in f:
        #     line = line.split(',')
        #     if line[0] == user and sha256_crypt.verify(pw, line[1]):
        #         print("success")
        #         success = True
        #         break

    if success:
        return redirect(url_for('userpage', username=username))
    else:
        return redirect(url_for('login', err='failed'))


@app.route('/review')
def leave_review():
    return render_template('review_form.html')


@app.route('/save_review', methods=['POST'])
def save_review():
    return 'Review Saved'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
