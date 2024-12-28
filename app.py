from flask import Flask, send_from_directory, request, jsonify
import openai

app = Flask(__name__)

# Set your OpenAI API key (replace with environment variable in production)
openai.api_key = "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"

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/message')
def message():
    return jsonify({"message": "Welcome to SFDC24 Assistant!"})

@app.route('/assistant', methods=['POST'])
def assistant():
    user_input = request.json.get('input')
    try:
        # Generate a response using OpenAI's GPT-4 API
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input}
            ]
        )
        assistant_response = response['choices'][0]['message']['content']
    except Exception as e:
        assistant_response = f"Error: {str(e)}"
    return jsonify({"response": assistant_response})

if __name__ == '__main__':
    app.run(debug=True)
