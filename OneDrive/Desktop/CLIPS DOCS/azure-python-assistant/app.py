from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Python Assistant Backend is running!"

@app.route('/assistant', methods=['POST'])
def assistant():
    user_input = request.json.get('input')
    response = f"Assistant Response: {user_input}"  # Replace with real assistant logic
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
