from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/form', methods=['GET', 'POST'])
def form_handler():
    if request.method == 'POST':
        # Handle POST request
        name = request.form.get('name', '')
        email = request.form.get('email', '')
        message = request.form.get('message', '')

        # Process the form data
        result = {
            'method': 'POST',
            'name': name,
            'email': email,
            'message': message
        }
        return render_template('result.html', result=result)

    else:  # GET request
        # You can access query parameters if there are any
        name = request.args.get('name', '')
        email = request.args.get('email', '')
        message = request.args.get('message', '')

        # Check if there are any query parameters
        if name or email or message:
            result = {
                'method': 'GET',
                'name': name,
                'email': email,
                'message': message
            }
            return render_template('result.html', result=result)

        # If no query parameters, show the form
        return render_template('form.html')


if __name__ == '__main__':
    app.run(debug=True)