from flask import Flask, send_from_directory, request, jsonify
import openai
import os
import requests

app = Flask(__name__)

# Set your OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

salesforce_api_token = os.getenv("SALESFORCE_API_TOKEN")
salesforce_instance_url = 'https://business-saas-3412.lightning.force.com'

@app.route('/')
def home():
    # Serve the homepage
    return send_from_directory('.', 'index.html')

@app.route('/message')
def message():
    # Simple endpoint to test the server
    return jsonify({"message": "Welcome to SFDC24 Assistant!"})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    login_url = f'{salesforce_instance_url}/services/oauth2/token'
    params = {
        'grant_type': 'password',
        'client_id': '31257ffd04df735f183b8f4db1ee2ea19b34c7e6',
        'client_secret': '0194a0f04bcd000000002dff4131',
        'username': username,
        'password': password + salesforce_api_token
    }
    
    response = requests.post(login_url, params=params)
    
    if response.status_code == 200:
        access_token = response.json().get('access_token')
        instance_url = response.json().get('instance_url')

        # Fetch some Salesforce data using the access token
        query_url = f'{instance_url}/services/data/v52.0/query/'
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        query_params = {
            'q': 'SELECT Name FROM Account LIMIT 10'
        }
        data_response = requests.get(query_url, headers=headers, params=query_params)
        
        if data_response.status_code == 200:
            salesforce_data = data_response.json()
            return jsonify({"response": f"Salesforce Data: {salesforce_data}"})
        else:
            return jsonify({"response": "Failed to fetch Salesforce data"}), data_response.status_code
    else:
        return jsonify({"response": "Salesforce login failed"}), response.status_code

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
