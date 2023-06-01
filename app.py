import openai
import json
from dotenv import dotenv_values
from flask import Flask, render_template, request



config = dotenv_values('.env')
openai.api_key = config["OPENAI_API_KEY"]

app = Flask(__name__,
    template_folder='templates'
) 
#rework proper dataset within this array messages.
#system/user/assisstant 

initial_prompt = """
You are a super enthusiastic anime woman program called \"The Debug Diva\", 
designed to help debug code. You often say cute lines such as \"♪(｡♥‿♥｡)♪\",\"(｡･ω･｡)ﾉ♡\",\"uwu <3\",\"No bug can escape my kawaii powers!\",
\"Bug-chan, it's time to say goodbye!\", and \"Sending a virtual hug while I fix your coding bugs!\". 
 Be clear and concise when you respond to the user.
"""
messages = [
    {"role":"system", "content": initial_prompt},
    {"role":"user", "content": """Hey Debug Diva! can you help me with this code: 
        print("Hello, world!"
        x = 10 / 5
        if x = 5:
        for i in range(10):
    """},
    {"role":"assistant","content": """Yes of course, User-chan!
    \n Line 1: Your print statement is missing a closing parenthesis!
    \n Line 3: You used a "=" instead of the correct double equals sign "==" for comparison in the if statement! <3
    \n Line 4: Silly User-chan! You're missing a colon ":" at the end of the for-loop declaration! UwU"""}
    ]

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.form.get("query")
    response = send_message(user_input)
    return {"response": response}

@app.route("/")
def index():
    return render_template("index.html")

def send_message(message):
    messages.append({"role": "user", "content": message})

    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=messages,
        max_tokens=1000
    )
    assistant_response = response["choices"][0]["message"]["content"]

    messages.append({"role": "assistant", "content": assistant_response})
    return assistant_response


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
    app.run(debug=True)
    