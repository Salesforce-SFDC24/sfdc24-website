from flask import Flask, send_from_directory, request, jsonify
import openai

app = Flask(__name__)

# Set your OpenAI API key (replace with environment variable in production)
openai.api_key = "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"

@app.route('/')
def home():
    # Serve the homepage
    return send_from_directory('.', 'index.html')

@app.route('/message')
def message():
    # Simple endpoint to test the server
    return jsonify({"message": "Welcome to SFDC24 Assistant!"})

@app.route('/assistant', methods=['POST'])
def assistant():
    """
    Endpoint to handle user input and generate a response
    using OpenAI's GPT model.
    """
    user_input = request.json.get('input')  # Capture the user input from the request
    try:
        # Generate a response using OpenAI's GPT-4 API
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input}
            ]
        )
        # Extract the assistant's response
        assistant_response = response['choices'][0]['message']['content']
    except Exception as e:
        # Handle errors with a user-friendly message
        assistant_response = f"Sorry, I couldn't process your request. Error: {str(e)}"
    
    return jsonify({"response": assistant_response})

if __name__ == '__main__':
    # Run the Flask app in debug mode
    app.run(debug=True)
