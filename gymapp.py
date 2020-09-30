import flask

from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename

app = Flask(__name__)


@app.route('/')
def home_page():
    return render_template('home_page.html')


@app.route('/create_account')
def create_account():
    return render_template('account_form.html')


@app.route('/account_complete',  methods=['POST'])
def account_complete():
    user = request.form['username']
    pw = request.form['password']
    email = request.form["email"]
    with open('users.txt', 'a') as f:
        f.write(user+','+pw+','+email)
        f.write('\n')
    return redirect(url_for('userpage', username=user))


@app.route('/u/<username>')
def userpage(username):
    return render_template('userpage.html', name=username)

@app.route('/login')
@app.route('/login/<err>')
def login(err='none'):
    print(err, type(err))
    return render_template('login.html', error=err)


@app.route('/login/authentication', methods=['POST'])
def login_auth():
    user = request.form["username"]
    pw = request.form["password"]
    success = False
    with open('users.txt', 'r') as f:
        for line in f:
            line = line.split(',')
            if line[0] == user and line[1] == pw:
                print("success")
                success = True
                break
    if success:
        return redirect(url_for('userpage', username=user))
    else:
        return redirect(url_for('login', err='failed'))


if __name__ == '__main__':
    app.run(debug=True)