# app.py
from flask import Flask, request, make_response, render_template, redirect, url_for

app = Flask(__name__)


@app.route('/')
def index():
    # Check if user has the cookie
    username = request.cookies.get('username')
    theme = request.cookies.get('theme', 'light')
    visit_count = request.cookies.get('visit_count', '0')

    # Increment visit counter
    new_count = int(visit_count) + 1

    # Create response object
    resp = make_response(render_template('index.html',
                                         username=username,
                                         theme=theme,
                                         visit_count=new_count))

    # Update visit counter cookie
    resp.set_cookie('visit_count', str(new_count), max_age=60 * 60 * 24 * 30)  # 30 days

    return resp


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        remember = request.form.get('remember') == 'on'

        resp = make_response(redirect(url_for('index')))

        if remember:
            # Set cookie to expire in 30 days
            resp.set_cookie('username', username, max_age=60 * 60 * 24 * 30)
        else:
            # Session cookie (expires when browser closes)
            resp.set_cookie('username', username)

        return resp

    return render_template('login.html')


@app.route('/logout')
def logout():
    resp = make_response(redirect(url_for('index')))
    resp.delete_cookie('username')
    return resp


@app.route('/preferences', methods=['GET', 'POST'])
def preferences():
    if request.method == 'POST':
        theme = request.form.get('theme', 'light')
        resp = make_response(redirect(url_for('index')))
        resp.set_cookie('theme', theme, max_age=60 * 60 * 24 * 365)  # 1 year
        return resp

    current_theme = request.cookies.get('theme', 'light')
    return render_template('preferences.html', theme=current_theme)


@app.route('/clear_all_cookies')
def clear_all_cookies():
    resp = make_response(redirect(url_for('index')))

    # Clear all cookies
    for cookie in request.cookies:
        resp.delete_cookie(cookie)

    return resp


if __name__ == '__main__':
    app.run(debug=True)