from flask import Flask, request, jsonify, send_from_directory,  render_template
import sys

from flask_cors import CORS

try:
    import flask_cors
    print("flask-cors is installed.")
except ImportError:
    print("flask-cors is NOT installed.")


app = Flask(__name__)
CORS(app)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    try:
        
        data = request.json
        print("Received data:", data)  # Debugging statement

        image_url = data.get('image_url')
        text = data.get('text')
        prompt = data.get('prompt')

        if not all([image_url, text, prompt]):
            return jsonify({"error": "All fields (image_url, text, prompt) are required."}), 400


        # Combine the inputs into a single prompt for the ChatGPT model
        combined_prompt = f"Image URL: {image_url}\nText: {text}\nPrompt: {prompt}"
        print("Combined prompt:", combined_prompt)  # Debugging statement


        from openai import OpenAI
        client = OpenAI()

        completion = client.chat.completions.create(
         model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
          #  {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
            {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
            ]
        )
        
     

        

        # Extract the message content from the response
        print (completion.choices)
        message_content = completion.choices[0].message.content.replace('\n', '<br>')

        return jsonify({"response": message_content})
    
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)