from flask import Flask, request, jsonify, send_from_directory,  render_template
import sys
from pathlib import Path

from flask_cors import CORS

try:
    import flask_cors
    print("flask-cors is installed.")
except ImportError:
    print("flask-cors is NOT installed.")


app = Flask(__name__)
CORS(app)

MAX_INPUT_LENGTH = 4096  # Define maximum input length

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
        language = data.get('language')
        print(language)

        if not all([image_url, text, prompt]):
            return jsonify({"error": "All fields (image_url, text, prompt) are required."}), 400


        # Combine the inputs into a single prompt for the ChatGPT model
        combined_prompt = f"{image_url} {text} {prompt}"
        combined_prompt = f"Compose a 600 word story for kids with facts in {language} that is about " + combined_prompt
        print("Combined prompt:", combined_prompt)  # Debugging statement


        from openai import OpenAI
        client = OpenAI()
        
        print(len(combined_prompt))
        completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a writer  assistant, skilled in creating fiction stories."},
          #  {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
            {"role": "user", "content": combined_prompt}
            ],
         max_tokens=1500  # Set the maximum number of tokens in the response   
        )
        
     

        

        # Extract the message content from the response
        print (completion.choices)
        message_content = completion.choices[0].message.content.replace('\n', '<br>')
        print(len(message_content))
        if len(message_content) > MAX_INPUT_LENGTH:
            message_content = message_content[:MAX_INPUT_LENGTH] 
        print(len(message_content))
         
        
        speech_file_path = Path(__file__).parent / "speech.mp3"
        response_audio = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=message_content
)
        with open(speech_file_path, 'wb') as f:
            for chunk in response_audio.iter_bytes():
                f.write(chunk)
       # response_audio.stream_to_file(speech_file_path)
        print(speech_file_path)

        return jsonify({"response": message_content})
    
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500

@app.route('/audio')
def audio():
    return send_from_directory(directory=Path(__file__).parent, path='speech.mp3')




if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)