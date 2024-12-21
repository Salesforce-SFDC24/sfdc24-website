from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    message = get_message()
    return render_template("index.html", message=message)

def get_message():
    return "Hello from Python!"

@app.route('/assistant', methods=['POST'])
def assistant():
    user_input = request.json.get('input')
    response = f"Assistant Response: {user_input}"  # Replace with real assistant logic
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
