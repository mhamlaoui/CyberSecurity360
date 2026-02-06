import os
from flask import Flask, render_template, request
import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm.base import LLM  # <-- Important
from transformers import pipeline

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs("static", exist_ok=True)

# Hugging Face pipeline
huggingface_model = pipeline('text-generation', model='tiiuae/falcon-rw-1b')

# ✅ Définir un LLM personnalisé
class CustomLLM(LLM):
    def call(self, prompt: str, **kwargs):
        print("Prompt envoyé au LLM:", prompt)
        return huggingface_model(prompt, max_new_tokens=100)[0]['generated_text']

# ✅ Initialiser une instance de CustomLLM
custom_llm = CustomLLM()

# Variable globale
df = None

@app.route('/', methods=['GET', 'POST'])
def chat():
    global df
    chat_history = []

    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            if file.filename.endswith('.csv'):
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(filepath)
                df = pd.read_csv(filepath)
                chat_history.append(('user', f'Fichier {file.filename} chargé. Pose ta question.'))

        elif 'prompt' in request.form:
            prompt = request.form['prompt']
            if df is not None:
                pandas_ai = SmartDataframe(df, config={"llm": custom_llm})
                result = pandas_ai.chat(prompt)
                chat_history.append(('user', prompt))

                if os.path.exists("static/chart.png"):
                    chat_history.append(('bot', 'image'))
                else:
                    chat_history.append(('bot', result))
            else:
                chat_history.append(('bot', "Veuillez d'abord uploader un fichier CSV."))

    return render_template('index.html', chat_history=chat_history)

if __name__ == '__main__':
    app.run(debug=True)
