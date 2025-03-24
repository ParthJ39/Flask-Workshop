from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Flask Dynamic Routes Demo</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                line-height: 1.6;
            }
            h1 {
                color: #3498db;
            }
            .card {
                background-color: white;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                padding: 20px;
                margin-bottom: 20px;
            }
            .links {
                display: flex;
                flex-wrap: wrap;
                gap: 10px;
                margin-top: 20px;
            }
            .link {
                display: inline-block;
                background-color: #3498db;
                color: white;
                padding: 10px 15px;
                border-radius: 5px;
                text-decoration: none;
                transition: background-color 0.3s;
            }
            .link:hover {
                background-color: #2980b9;
            }
        </style>
    </head>
    <body>
        <h1>Flask Dynamic Routes Demo</h1>

        <div class="card">
            <h2>User Profiles</h2>
            <p>Check out these example user profiles:</p>
            <div class="links">
                <a href="/user/john" class="link">John's Profile</a>
                <a href="/user/sarah" class="link">Sarah's Profile</a>
                <a href="/user/alex" class="link">Alex's Profile</a>
            </div>
        </div>

        <div class="card">
            <h2>Blog Posts</h2>
            <p>View these example blog posts:</p>
            <div class="links">
                <a href="/post/1" class="link">Post #1</a>
                <a href="/post/42" class="link">Post #42</a>
                <a href="/post/999" class="link">Post #999</a>
            </div>
        </div>
    </body>
    </html>
    '''


@app.route('/user/<username>')
def show_user(username):
    # Render the user template with the username parameter
    return render_template('user.html', username=username)


@app.route('/post/<int:post_id>')
def show_post(post_id):
    # Render the post template with the post_id parameter
    return render_template('post.html', post_id=post_id)


if __name__ == '__main__':
    app.run(debug=True)