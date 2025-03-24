from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return "Home Page"

@app.route('/login')
def login():
    return "Login Page"

@app.route('/user/<username>')
def profile(username):
    return f"Profile page for {username}"

@app.route('/post/<int:post_id>')
def show_post(post_id):
    return f"Post #{post_id}"

@app.route('/category/<category>/tag/<tag>')
def category_tag(category, tag):
    return f"Category: {category}, Tag: {tag}"

@app.route('/search')
def search():
    return "Search Results"

# Test the URL generation outside of a request context
with app.test_request_context():
    print("Generated URLs:")
    print(f"home: {url_for('home')}")
    print(f"login: {url_for('login')}")
    print(f"profile: {url_for('profile', username='John')}")
    print(f"show_post: {url_for('show_post', post_id=42)}")
    print(f"category_tag: {url_for('category_tag', category='python', tag='flask')}")
    print(f"search: {url_for('search')}")
    print(f"search with query: {url_for('search', q='flask tutorial', page=2)}")

if __name__ == '__main__':
    app.run(debug=True)