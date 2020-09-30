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
    user = request.form["username"]
    pw = request.form["password"]
    email = request.form["email"]
    with open('users.txt', 'a') as f:
        f.write(user+','+pw+','+email)
        f.write('\n')
    return render_template('account_complete.html', name=user)


if __name__ == '__main__':
    app.run(debug=True)