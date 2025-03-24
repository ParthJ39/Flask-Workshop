from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route('/')
def home():
    # Generate URLs using url_for instead of hardcoding them
    user_links = [
        {'name': 'John', 'url': url_for('show_user', username='john')},
        {'name': 'Sarah', 'url': url_for('show_user', username='sarah')},
        {'name': 'Alex', 'url': url_for('show_user', username='alex')}
    ]

    post_links = [
        {'id': 1, 'url': url_for('show_post', post_id=1)},
        {'id': 42, 'url': url_for('show_post', post_id=42)},
        {'id': 999, 'url': url_for('show_post', post_id=999)}
    ]

    return render_template('home.html', user_links=user_links, post_links=post_links)


@app.route('/user/<username>')
def show_user(username):
    # Pass the home URL using url_for
    home_url = url_for('home')
    return render_template('user.html', username=username, home_url=home_url)


@app.route('/post/<int:post_id>')
def show_post(post_id):
    # Pass the home URL using url_for
    home_url = url_for('home')
    return render_template('post.html', post_id=post_id, home_url=home_url)

if __name__ == '__main__':
    app.run(debug=True)