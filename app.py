from flask import Flask, send_from_directory, request, jsonify
import openai
import os

app = Flask(__name__)

# Set your OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

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
        # Check if the user is requesting image generation
        if user_input.lower().startswith("generate image of"):
            description = user_input[len("generate image of "):]
            response = openai.Image.create(
                prompt=description,
                n=1,
                size="1024x1024"
            )
            image_url = response['data'][0]['url']
            assistant_response = f"<img src='{image_url}' alt='Generated Image' />"
        else:
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
