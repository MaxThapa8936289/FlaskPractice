from flask import Flask, redirect, url_for, request, render_template, session
from passlib.hash import sha256_crypt
import pymysql

app = Flask(__name__)
app.secret_key = 'MyGymFlaskKey'


def fetch_review():
    # Fetch Review for display
    connection = pymysql.connect(host='54.243.215.108',
                                 user='user2',
                                 password='password2',
                                 db='reviews')
    try:
        with connection.cursor() as cursor:
            # Fetch password hash based on user
            sql = "SELECT * FROM anonreviews;"
            cursor.execute(sql)
            review_data = cursor.fetchall()
    finally:
        connection.close()

    day = []
    date = []
    message = []

    for data in review_data:
        day.append(data[0].strftime("%A"))
        date.append(data[0].strftime("%x"))
        message.append(data[4])

    return day, date, message


@app.route('/')
def index():
    day, date, message = fetch_review()
    return render_template('index.html', day=day, date=date, message=message)


@app.route('/create_account')
def create_account():
    return render_template('account_form.html')


@app.route('/check/<uname>')
def check(uname):
    name_check = ''
    connection = pymysql.connect(host='54.243.215.108',
                                 user='user2',
                                 password='password2',
                                 db='userdata')
    try:
        with connection.cursor() as cursor:
            # Fetch password hash based on user
            sql = "SELECT username FROM userlogin;"
            cursor.execute(sql)
            users = cursor.fetchall()
            name_check = (uname.strip(),)
    finally:
        connection.close()

    if name_check in users:
        return "unavailable"
    else:
        return "available"


@app.route('/account_complete', methods=['POST'])
def account_complete():
    username = request.form['username']
    password = sha256_crypt.hash(request.form['password'])
    email = request.form["email"]
    session['username'] = username  # Initiate user session

    # Add account to records
    connection = pymysql.connect(host='54.243.215.108',
                                 user='user2',
                                 password='password2',
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
    if 'username' in session:
        username = session['username']
        return render_template('logged_in.html', name=username)
    else:
        return render_template('login.html', error=err)


@app.route('/login/authentication', methods=['POST'])
def login_auth():
    username = request.form["username"]
    password = request.form["password"]
    success = False

    connection = pymysql.connect(host='54.243.215.108',
                                 user='user2',
                                 password='password2',
                                 db='userdata')
    try:
        with connection.cursor() as cursor:
            # Fetch password hash based on user
            sql = "SELECT password FROM userlogin WHERE username = %s;"
            if cursor.execute(sql, username) == 1:  # username exists in database
                pw_hash = cursor.fetchone()[0]
                # verify password
                if sha256_crypt.verify(password, pw_hash):
                    success = True
            else:
                pass
    finally:
        connection.close()

    if success:
        session['username'] = username  # Initiate user session
        return redirect(url_for('userpage', username=username))
    else:
        return redirect(url_for('login', err='failed'))


@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/review')
def leave_review():
    return render_template('review_form.html')


@app.route('/save_review', methods=['POST'])
def save_review():
    gender = request.form['gender']
    dob = request.form['DOB']
    review = request.form["message"]

    # Add account to records
    connection = pymysql.connect(host='54.243.215.108',
                                 user='user2',
                                 password='password2',
                                 db='reviews')
    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO anonreviews (Date, Time, Gender, DOB, Message) " \
                  "VALUES (CURDATE(), CURTIME(), %s, %s, %s);"
            cursor.execute(sql, (gender, dob, review))
        # Save changes
        connection.commit()
    finally:
        connection.close()

    return redirect(url_for('thank_feedback'))


@app.route('/review/thankyou')
def thank_feedback():
    return render_template('thanks_feedback.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
