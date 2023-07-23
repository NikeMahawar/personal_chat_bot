import os
from flask import Flask, render_template, request, send_file
import openai

OPENAI_API_KEY = "Your_OPENAI_API_KEY"

app = Flask(__name__)

openai.api_key = OPENAI_API_KEY

MODEL_PROMPT = "You are a helpful assistant.\nYou can answer questions and have a conversation with me.\n\nUser: "
chat_history = []

def get_chatbot_response(user_input):
    combined_input = MODEL_PROMPT + user_input

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=combined_input,
        max_tokens=4000,
        stop=["\nUser:", "\nBot:"],
    )

    # Extract the response from the API response
    chatbot_response = response["choices"][0]["text"].strip()

    return chatbot_response

# Home route to render the chat UI
@app.route('/')
def home():
    return render_template('index.html', chat_history=chat_history)

# Route to handle user input and chatbot response
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']
    chat_history.append({'user': user_input})
    bot_response = get_chatbot_response(user_input)
    chat_history.append({'bot': bot_response})
    return render_template('index.html', chat_history=chat_history)

# Route to serve the HTML file from the templates directory
@app.route('/index.html')
def get_html():
    return send_file('templates/index.html')

if __name__ == "__main__":
    app.run(debug=True)
