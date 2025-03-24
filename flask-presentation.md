# Flask Workshop: Web Development with Python

---

## Introduction to Flask

### What is Flask?
- Lightweight and flexible web framework for Python
- Micro-framework with minimal dependencies
- Ideal for both small and large applications
- Developed by Armin Ronacher in 2010

### Why Flask?
- Simple and easy to learn
- Highly customizable
- Great for RESTful APIs, web apps, and microservices
- Active community and excellent documentation
- Works well with other Python libraries

### Flask vs Other Frameworks
- Django: Full-featured but more complex
- FastAPI: Modern, async-focused
- Flask: Minimalist but extensible

**Hands-on Preparation:** Have students check Python installation using `python --version`

---

## Flask Environment Setup

### Setting Up the Environment

**Hands-on Task 1:** Create a virtual environment
```python
# Windows
python -m venv flask_env
flask_env\Scripts\activate

# macOS/Linux
python -m venv flask_env
source flask_env/bin/activate
```

**Hands-on Task 2:** Install Flask
```
pip install flask
```

**Hands-on Task 3:** Create your first Flask application (hello.py)
```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)
```

**Hands-on Task 4:** Run the application
```
python hello.py
```
- Visit http://127.0.0.1:5000/ in your browser

**Hands-on Task 5:** Modify the application to display your name and refresh

---

## App Routing

### Understanding URL Routing

**Hands-on Task 6:** Create multiple routes
```python
@app.route('/')
def home():
    return 'Home Page'

@app.route('/about')
def about():
    return 'About Page'

@app.route('/contact')
def contact():
    return 'Contact Page'
```

### Dynamic Routes

**Hands-on Task 7:** Create dynamic routes with parameters
```python
@app.route('/user/<username>')
def show_user(username):
    return f'User: {username}'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    return f'Post ID: {post_id}'
```

**Challenge:** Create a route that accepts two parameters and performs a calculation based on them

---

## URL Building

### Creating URLs Dynamically

**Hands-on Task 8:** Use `url_for()` to generate URLs
```python
from flask import Flask, url_for

@app.route('/')
def index():
    return 'Index Page'

@app.route('/login')
def login():
    return 'Login Page'

@app.route('/user/<username>')
def profile(username):
    return f'{username}\'s profile'

with app.test_request_context():
    print(url_for('index'))
    print(url_for('login'))
    print(url_for('profile', username='John'))
```

**Hands-on Task 9:** Create navigation links using url_for
```python
from flask import Flask, url_for

@app.route('/')
def index():
    login_url = url_for('login')
    profile_url = url_for('profile', username='student')
    return f'''
    <h1>Welcome to Flask</h1>
    <ul>
        <li><a href="{login_url}">Login</a></li>
        <li><a href="{profile_url}">Profile</a></li>
    </ul>
    '''
```

---

## Flask HTTP Methods

### Handling Different HTTP Methods

**Hands-on Task 10:** Create a form that handles GET and POST requests
```python
from flask import Flask, request, render_template_string

app = Flask(__name__)

form_template = '''
<!DOCTYPE html>
<html>
<head>
    <title>Flask Form Example</title>
</head>
<body>
    <h1>Flask Form Example</h1>
    <form method="POST">
        <label>Name: <input type="text" name="name"></label><br>
        <label>Email: <input type="email" name="email"></label><br>
        <input type="submit" value="Submit">
    </form>
    {% if name and email %}
    <h2>Submitted Data:</h2>
    <p>Name: {{ name }}</p>
    <p>Email: {{ email }}</p>
    {% endif %}
</body>
</html>
'''

@app.route('/form', methods=['GET', 'POST'])
def form():
    name = None
    email = None
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
    return render_template_string(form_template, name=name, email=email)
```

**Hands-on Task 11:** Test the form using both GET and POST methods

---

## Flask Request Object 

### Working with Request Data

**Hands-on Task 12:** Explore different aspects of the request object
```python
from flask import Flask, request

@app.route('/request-info')
def request_info():
    user_agent = request.headers.get('User-Agent')
    ip_address = request.remote_addr
    args = request.args
    
    return f'''
    <h1>Request Information</h1>
    <p><strong>User Agent:</strong> {user_agent}</p>
    <p><strong>IP Address:</strong> {ip_address}</p>
    <p><strong>Query Parameters:</strong> {args}</p>
    '''
```

**Hands-on Task 13:** Create an endpoint that can process JSON data
```python
from flask import Flask, request, jsonify

@app.route('/api/data', methods=['POST'])
def api_data():
    if request.is_json:
        data = request.get_json()
        # Process the data
        response = {
            "status": "success",
            "received_data": data,
            "message": "Data processed successfully"
        }
        return jsonify(response)
    else:
        return jsonify({"status": "error", "message": "Request must be JSON"}), 400
```

**Challenge:** Use Postman or curl to test the JSON endpoint

---

## Flask Cookies 

### Managing Cookies in Flask

**Hands-on Task 14:** Set and retrieve cookies
```python
from flask import Flask, request, make_response

@app.route('/set-cookie/<name>')
def set_cookie(name):
    resp = make_response(f'Cookie "{name}" set!')
    resp.set_cookie('user', name)
    return resp

@app.route('/get-cookie')
def get_cookie():
    user = request.cookies.get('user')
    if user:
        return f'Hello, {user}!'
    else:
        return 'No cookie found'

@app.route('/delete-cookie')
def delete_cookie():
    resp = make_response('Cookie deleted!')
    resp.delete_cookie('user')
    return resp
```

**Hands-on Task 15:** Create a simple page visit counter using cookies
```python
@app.route('/visit-counter')
def visit_counter():
    count = int(request.cookies.get('visit_count', 0))
    count += 1
    
    resp = make_response(f'You have visited this page {count} times')
    resp.set_cookie('visit_count', str(count))
    return resp
```

---

## File Uploading in Flask 

### Handling File Uploads

**Hands-on Task 16:** Create a file upload form
```python
from flask import Flask, request, render_template_string
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

upload_template = '''
<!DOCTYPE html>
<html>
<head>
    <title>File Upload</title>
</head>
<body>
    <h1>Upload a File</h1>
    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="file">
        <input type="submit" value="Upload">
    </form>
    {% if filename %}
    <h2>Uploaded: {{ filename }}</h2>
    {% endif %}
</body>
</html>
'''

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    filename = None
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        
        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    return render_template_string(upload_template, filename=filename)
```

**Hands-on Task 17:** Add file type validation
```python
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload-safe', methods=['GET', 'POST'])
def upload_file_safe():
    filename = None
    error = None
    
    if request.method == 'POST':
        if 'file' not in request.files:
            error = 'No file part'
        else:
            file = request.files['file']
            if file.filename == '':
                error = 'No selected file'
            elif not allowed_file(file.filename):
                error = 'File type not allowed'
            else:
                filename = file.filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    return render_template_string(
        upload_template.replace('{% if filename %}', 
                              '{% if error %}<p style="color: red;">Error: {{ error }}</p>{% endif %}{% if filename %}'),
        filename=filename, error=error)
```

---

## Final Hands-on Exercise

### Creating a Mini Blog Application

**Challenge:** Combine all the concepts to create a simple blog application with:
- Home page listing posts
- Form to create new posts
- Ability to upload an image with each post
- Using cookies to remember the user's name
- Proper URL routes for viewing individual posts

**Starting Code:**
```python
from flask import Flask, request, render_template_string, redirect, url_for, make_response
import os
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# In-memory database (for demo purposes)
posts = []

# Templates (would normally be in separate files)
# ... (provide template code)

# Routes to implement:
# 1. Home page
# 2. New post form
# 3. View individual post
# 4. Set username cookie
```

---

## Additional Resources

### For Further Learning
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask Mega-Tutorial by Miguel Grinberg](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
- [Flask Web Development with Python Tutorial](https://www.youtube.com/watch?v=Z1RJmh_OqeA)
- [Flask Extensions](https://flask.palletsprojects.com/en/2.0.x/extensions/)

### Recommended Extensions for Production
- Flask-SQLAlchemy: Database integration
- Flask-WTF: Form handling
- Flask-Login: User authentication
- Flask-Migrate: Database migrations
- Flask-RESTful: API building
