import openai
from flask import Flask, request, render_template, send_file
from dotenv import load_dotenv
import os

load_dotenv()

openai.api_key = os.environ.get('OPENAI_API_KEY')
model_engine = "text-davinci-002"

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    title = request.form['title']
    length = int(request.form['length'])
    language = request.form['language']
    text = generate_text(title, length, language)
    return render_template('generated.html', text=text)

def generate_text(title, length, language):
    prompt = f"Write an essay on the topic: {title}\n\nEssay:\n"
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=length,
        n=1,
        stop=None,
        temperature=0.7,
    )
    text = response.choices[0].text
    return text

@app.route('/download')
def download():
    title = request.args.get('title')
    length = int(request.args.get('length'))
    language = request.args.get('language')
    text = generate_text(title, length, language)
    filename = f"{title.replace(' ', '_')}.txt"
    with open(filename, 'w') as f:
        f.write(text)
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run()
