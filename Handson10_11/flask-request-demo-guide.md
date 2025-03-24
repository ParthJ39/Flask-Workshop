# Flask Request Object Demo: Step-by-Step Guide

## Step 1: Setup and Introduction
1. Run the application with `python app.py`
2. Open http://localhost:5000 in your browser
3. Today we're exploring Flask's request object, which gives us access to all HTTP request data sent by clients

## Step 2: Basic Request Properties Demonstration
1. Click "Submit GET Request" on the home page without changing any values
2. Notice the parameters in the URL: `?name=John&age=25`
3. Flask captures these through `request.method`, `request.path`, and `request.url`
4. The request object tells us this is a GET request to the /request-info path

## Step 3: Query Parameters (GET data)
1. Look at the Query Parameters section in the results
2. These values come from `request.args` which captures all URL parameters
3. Code: `query_params = dict(request.args)`
4. If we needed just one value, we could use `request.args.get('name')`
5. Try modifying the form values and submit again to see how `request.args` changes

## Step 4: Form Data (POST data)
1. Go back to the home page
2. Fill in the second form and click "Submit POST Request"
3. Notice the URL has no parameters this time
4. Look at the Form Data section in the results
5. POST data is captured via `request.form` instead of `request.args`
6. Code: `form_data = dict(request.form)`
7. This is more secure for sensitive data like passwords

## Step 5: Client Information
1. Look at the Client Information section
2. Flask captures client details like IP address with `request.remote_addr`
3. The User-Agent header comes from `request.headers.get('User-Agent')`
4. The IP and user agent are useful for logging, analytics, and security

## Step 6: Headers Exploration
1. Look at the Headers section
2. HTTP headers contain metadata about the request
3. Code: `all_headers = dict(request.headers)`
4. Individual headers can be accessed via `request.headers.get('Header-Name')`
5. Headers can indicate content type, authentication, caching preferences, etc.

## Step 7: JSON Data Demonstration (using curl)
1. Open a terminal
2. Run the curl command shown on the home page:
   ```
   curl -X POST -H "Content-Type: application/json" -d '{"message":"Hello","priority":"high"}' http://localhost:5000/request-info
   ```
3. Look for the JSON Data section in output (or copy from terminal)
4. Flask detects JSON with `request.is_json` and parses it using `request.get_json()`
5. This is essential for modern APIs that work with JSON data

## Step 8: Custom Headers Demonstration
1. Run the second curl command:
   ```
   curl -H "X-Custom-Header: Special-Value" http://localhost:5000/request-info
   ```
2. Notice the Custom Header value in the results
3. Applications can use custom headers for authentication tokens, API keys, etc.
4. Code: `custom_header = request.headers.get('X-Custom-Header', 'Not provided')`

## Step 9: Cookies and State
1. Although not demonstrated directly, cookies can be accessed via `request.cookies`
2. Code: `cookies = dict(request.cookies)`
3. Cookies help maintain state between requests for things like sessions and preferences

## Step 10: Practical Applications
1. Key parts of the request object:
   - `request.method` for handling different HTTP methods
   - `request.args` for URL parameters
   - `request.form` for form submissions
   - `request.get_json()` for API requests
   - `request.headers` for metadata and authentication
   - `request.remote_addr` for logging and security

2. Real-world uses:
   - Building REST APIs with different endpoints for different methods
   - Processing form submissions securely
   - Validating user input before processing
   - Implementing authentication systems
   - Handling file uploads with `request.files`

## Step 11: Security Considerations
1. Always validate and sanitize data from request objects
2. Never trust client-side data without validation
3. Flask provides tools to safely access request data, but validation logic is up to you
