from flask import Flask, request, render_template_string

app = Flask(__name__)


@app.route('/')
def index():
    # Simple form that will submit to our request-info endpoint
    return '''
    <h1>Flask Request Object Demo</h1>
    <p>Explore different aspects of the Flask request object.</p>

    <h2>GET request with query parameters</h2>
    <form action="/request-info" method="get">
        <label>Name: <input type="text" name="name" value="John"></label><br>
        <label>Age: <input type="number" name="age" value="25"></label><br>
        <input type="submit" value="Submit GET Request">
    </form>

    <h2>POST request with form data</h2>
    <form action="/request-info" method="post">
        <label>Username: <input type="text" name="username" value="user123"></label><br>
        <label>Password: <input type="password" name="password" value="secret"></label><br>
        <label>Remember me: <input type="checkbox" name="remember" checked></label><br>
        <input type="submit" value="Submit POST Request">
    </form>

    <h2>POST request with file upload</h2>
    <form action="/request-info" method="post" enctype="multipart/form-data">
        <label>Upload a file: <input type="file" name="file"></label><br>
        <input type="submit" value="Submit File">
    </form>

    <h2>POST request with JSON data</h2>
    <p>Use Postman or curl to send a POST request with JSON data to /request-info</p>
    <code>curl -X POST -H "Content-Type: application/json" -d '{"message":"Hello"}' http://localhost:5000/request-info</code>

    <h2>Set Cookies</h2>
    <p><a href="/set-cookies">Click here to set cookies</a></p>
    '''


@app.route('/set-cookies')
def set_cookies():
    resp = app.make_response("Cookies have been set!")
    resp.set_cookie('user_id', '12345')
    resp.set_cookie('session_id', 'abc123')
    return resp


@app.route('/request-info', methods=['GET', 'POST'])
def request_info():
    # Basic request properties
    method = request.method
    path = request.path
    url = request.url

    # Headers
    user_agent = request.headers.get('User-Agent', 'Unknown')
    content_type = request.headers.get('Content-Type', 'Not specified')
    custom_header = request.headers.get('X-Custom-Header', 'Not provided')

    # IP address
    ip_address = request.remote_addr

    # Query parameters and form data
    query_params = dict(request.args)
    form_data = dict(request.form)

    # File uploads
    files = {k: f.filename for k, f in request.files.items()} if request.files else {}

    # Cookies
    cookies = dict(request.cookies)

    # JSON data
    json_data = request.get_json(silent=True) if request.is_json else None

    # Raw data
    raw_data = request.get_data(as_text=True)

    # Response
    response = f'''
    <h1>Request Information</h1>

    <h2>Basic Properties</h2>
    <ul>
        <li><strong>Method:</strong> {method}</li>
        <li><strong>Path:</strong> {path}</li>
        <li><strong>Full URL:</strong> {url}</li>
    </ul>

    <h2>Client Information</h2>
    <ul>
        <li><strong>IP Address:</strong> {ip_address}</li>
        <li><strong>User Agent:</strong> {user_agent}</li>
    </ul>

    <h2>Headers</h2>
    <ul>
        <li><strong>Content Type:</strong> {content_type}</li>
        <li><strong>Custom Header:</strong> {custom_header}</li>
    </ul>

    <h2>Data</h2>
    <ul>
        <li><strong>Query Parameters:</strong> <pre>{query_params}</pre></li>
        <li><strong>Form Data:</strong> <pre>{form_data}</pre></li>
        <li><strong>JSON Data:</strong> <pre>{json_data}</pre></li>
        <li><strong>Files:</strong> <pre>{files}</pre></li>
        <li><strong>Raw Data:</strong> <pre>{raw_data}</pre></li>
    </ul>

    <h2>Cookies</h2>
    <pre>{cookies}</pre>

    <p><a href="/">Back to Home</a></p>
    '''
    return response


if __name__ == '__main__':
    app.run(debug=True)