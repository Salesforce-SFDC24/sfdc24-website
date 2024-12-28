from flask import Flask, send_from_directory, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    message = get_message()
    return send_from_directory('.', 'index.html')

@app.route('/message')
def message():
    return jsonify({"message": "Hello from Python! this is a test for new branch"})

def get_message():
    return "Hello from Python! test new branch"

@app.route('/assistant', methods=['POST'])
def assistant():
    user_input = request.json.get('input')
    response = f"Assistant Response: {user_input}"  # Replace with real assistant logic
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
