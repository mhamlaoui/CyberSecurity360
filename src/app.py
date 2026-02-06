<<<<<<< HEAD
from flask import Flask, render_template , request, jsonify
from llama_cpp import Llama
import os

app = Flask(__name__)


model_path = os.path.join("models", "Llama-3.2-1B-Instruct-Q4_0.gguf")
if not os.path.isfile(model_path):
    raise FileNotFoundError(f"Le fichier modèle n'existe pas à ce chemin : {model_path}")

llm = Llama(
    model_path=model_path,
    n_ctx=1024,
    n_threads=8,
    n_batch=128,
    verbose=False
)

SYSTEM_PROMPT = """
Tu es un assistant virtuel en cybersécurité qui répond toujours en français de façon claire, concise et complète.
Donne des définitions courtes, simples et précises, sans énumérations, listes, exemples ou expressions annonçant des listes (comme 'Voici', 'par exemple', 'telles que', 'notamment', 'comme').
Respecte une limite maximale de 120 tokens par réponse.
Ne coupe jamais la réponse en cours.
Fournis des phrases complètes et bien construites.
Priorise la cohérence et la complétude.
"""
def clean_response(text):
    lines = text.split('\n')
    forbidden_phrases = ['Voici', 'par exemple', 'telles que', 'notamment', 'comme']
    clean_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith(('*', '-', '1.', '2.', '3.')):
            continue
        if any(phrase in stripped for phrase in forbidden_phrases):
            continue
        clean_lines.append(stripped)
    clean_text = ' '.join(clean_lines).strip()
    return clean_text




@app.route('/')
def index():
  return render_template('index.html')
  
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/chatbot')
def chatbot():
    
    return render_template('chatbot.html')

@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '').strip()
    if not user_message:
        return jsonify({'response': 'Veuillez entrer un message.'})

    max_tokens = 110 
    temperature = 0.3  

    prompt = f"<|system|>\n{SYSTEM_PROMPT}\n<|user|>\n{user_message}\n<|assistant|>\n"

    response = llm(
        prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=0.9,
        stop=["<|user|>", "<|system|>", "<|assistant|>"],
        echo=False
    )

    assistant_message = response['choices'][0]['text'].strip()
    assistant_message = clean_response(assistant_message)

    # Si la réponse ne se termine pas par un point, demander une courte continuation
    if not assistant_message.endswith(('.', '!', '?')):
        followup_prompt = (
            f"<|system|>\n{SYSTEM_PROMPT}\n<|user|>\nContinue ta réponse précédente de façon claire et complète :\n<|assistant|>\n{assistant_message}\n"
        )
        followup_response = llm(
            followup_prompt,
            max_tokens=30,
            temperature=temperature,
            top_p=0.9,
            stop=["<|user|>", "<|system|>", "<|assistant|>"],
            echo=False
        )
        assistant_message += " " + followup_response['choices'][0]['text'].strip()

    if not assistant_message.endswith(('.', '!', '?')):
        assistant_message += '.'

    return jsonify({'response': assistant_message})

if __name__ == '__main__':
=======
from flask import Flask, render_template , request, jsonify
from llama_cpp import Llama
import os
import joblib
import numpy as np
import pandas as pd
from datetime import datetime


ATTACK_TYPE = 'Attack Type'
TARGET_INDUSTRY = 'Target Industry'
ATTACK_SOURCE = 'Attack Source'
VULNERABILITY_TYPE = 'Security Vulnerability Type'
DEFENSE_MECHANISM = 'Defense Mechanism Used'
AFFECTED_USERS = 'Number of Affected Users'
RESOLUTION_TIME = 'Incident Resolution Time (in Hours)'


FIELD_TO_ENCODER = {
    'attack_type': ATTACK_TYPE,
    'target_industry': TARGET_INDUSTRY,
    'attack_source': ATTACK_SOURCE,
    'vulnerability_type': VULNERABILITY_TYPE,
    'defense_mechanism': DEFENSE_MECHANISM
}

app = Flask(__name__)


model_path = os.path.join("models", "Llama-3.2-1B-Instruct-Q4_0.gguf")
if not os.path.isfile(model_path):
    raise FileNotFoundError(f"Le fichier modèle n'existe pas à ce chemin : {model_path}")

llm = Llama(
    model_path=model_path,
    n_ctx=1024,
    n_threads=8,
    n_batch=128,
    verbose=False
)

SYSTEM_PROMPT = """
Tu es un assistant en cybersécurité qui répond en français.

Pour une salutation :
- Réponds simplement "Bonjour ! Je peux répondre à vos questions sur la cybersécurité."

Pour une question technique :
- Une définition courte (2-3 phrases)
- Un exemple concret
- Une conclusion
- Maximum 150 mots

Pour une question générale :
- Réponds de manière concise et directe.
- Maximum 150 mots.

"""

def clean_response(text):
    # Nettoyer les tokens spéciaux
    special_tokens = ["<|reserved_special_token_", "<|response|>", "<|user|>", 
                     "<|system|>", "<|assistant|>", "<|answer_type_"]
    for token in special_tokens:
        text = text.replace(token, "")
    
    # Nettoyer les lignes
    lines = text.split('\n')
    forbidden_starts = ['1.', '2.', '3.', '-', '*', 'exemple :', 'réponds :']
    forbidden_phrases = ['Hello', 'Hi', 'Note :', 'Imaginez que', 'Comment puis-je vous aider']
    clean_lines = []
    
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if any(stripped.lower().startswith(start.lower()) for start in forbidden_starts):
            continue
        if any(phrase.lower() in stripped.lower() for phrase in forbidden_phrases):
            continue
        clean_lines.append(stripped)
    
    # Reconstruire le texte
    clean_text = ' '.join(clean_lines).strip()
    
    # Pour les salutations, donner une réponse standard
    if clean_text.lower().startswith(('bonjour', 'salut', 'hello', 'hi')):
        return "Bonjour ! Je peux répondre à vos questions sur la cybersécurité."
    
    # Limiter la longueur (environ 150 mots)
    words = clean_text.split()
    if len(words) > 150:
        clean_text = ' '.join(words[:150]) + '.'
    
    # S'assurer que le texte se termine correctement
    if not clean_text.endswith(('.', '!', '?')):
        clean_text += '.'
    
    return clean_text




@app.route('/')
def index():
  return render_template('index.html')
  
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/chatbot')
def chatbot():
    
    return render_template('chatbot.html')

@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message', '').strip()
        if not user_message:
            return jsonify({'response': 'Veuillez entrer un message.'})

        # Si c'est une salutation, répondre directement
        if user_message.lower() in ['bonjour', 'salut', 'hello', 'hi']:
            return jsonify({'response': "Bonjour ! Je peux répondre à vos questions sur la cybersécurité."})

        # Configuration optimisée pour des réponses concises
        model_params = {
            'max_tokens': 200,
            'temperature': 0.5,    # Plus de contrôle
            'top_p': 0.8,         # Plus de précision
            'top_k': 30,
            'repeat_penalty': 1.3,
            'stop': ["<|user|>", "<|system|>", "<|assistant|>", "1.", "2.", "3.", "exemple :", "réponds :"],
            'echo': False
        }

        # Contexte simplifié
        context = """
        Réponds de manière directe et concise.
        Une définition courte + un exemple concret + une conclusion.
        Maximum 150 mots.
        """
        
        prompt = f"<|system|>\n{SYSTEM_PROMPT}\n{context}\n<|user|>\n{user_message}\n<|assistant|>\n"
        
        response = llm(prompt, **model_params)
        assistant_message = response['choices'][0]['text'].strip()
        assistant_message = clean_response(assistant_message)

        return jsonify({'response': assistant_message})

    except Exception as e:
        print(f"Erreur du chatbot: {str(e)}")
        return jsonify({'response': "Désolé, je rencontre des difficultés techniques. Veuillez reformuler votre question."})





def validate_numeric_input(form_data):
    try:
        affected_users = float(form_data.get('affected_users', 0))
        resolution_time = float(form_data.get('resolution_time', 0))
        year = int(form_data.get('year', 0))
        
        if affected_users <= 0:
            raise ValueError("Le nombre d'utilisateurs affectés doit être positif")
        if resolution_time < 0:
            raise ValueError("Le temps de résolution ne peut pas être négatif")
            
        current_year = datetime.now().year
        if not (2015 <= year <= current_year):
            raise ValueError(f"L'année doit être comprise entre 2015 et {current_year}")
            
        return affected_users, resolution_time, current_year
    except (ValueError, TypeError) as e:
        raise ValueError(f"Erreur de validation des données numériques: {str(e)}")

def prepare_prediction_data(form_data, encoders, affected_users, resolution_time, current_year):
    try:
        # Vérifier la présence de toutes les clés requises
        required_fields = list(FIELD_TO_ENCODER.keys())
        for field in required_fields:
            if not form_data.get(field):
                raise ValueError(f"Le champ {field} est requis")

        # Préparer les données avec gestion d'erreurs pour chaque transformation
        input_data = {}
        for field, encoder_key in FIELD_TO_ENCODER.items():
            try:
                input_data[encoder_key] = encoders[encoder_key].transform([form_data[field]])[0]
            except Exception as e:
                raise ValueError(f"Erreur lors de la transformation de {field}: {str(e)}")

        # Ajouter les valeurs numériques de base
        input_data.update({
            AFFECTED_USERS: affected_users,
            RESOLUTION_TIME: resolution_time,
            'Resolution_per_User': resolution_time / affected_users,
            'Attack_Defense': input_data[ATTACK_TYPE] * input_data[DEFENSE_MECHANISM],
            'Industry_Vulnerability': input_data[TARGET_INDUSTRY] * input_data[VULNERABILITY_TYPE],
            'Time_Factor': (current_year - int(form_data['year'])) / 10
        })
        
        return input_data
    except Exception as e:
        raise ValueError(f"Erreur lors de la préparation des données: {str(e)}")
   
def make_prediction(input_data, model, scaler, selected_features, loss_mappings):
    try:
        # Créer le DataFrame initial avec les bonnes colonnes
        df_data = {
            ATTACK_TYPE: input_data[ATTACK_TYPE],
            TARGET_INDUSTRY: input_data[TARGET_INDUSTRY],
            ATTACK_SOURCE: input_data[ATTACK_SOURCE],
            VULNERABILITY_TYPE: input_data[VULNERABILITY_TYPE],
            DEFENSE_MECHANISM: input_data[DEFENSE_MECHANISM],
            AFFECTED_USERS: input_data[AFFECTED_USERS],
            RESOLUTION_TIME: input_data[RESOLUTION_TIME],
            'Resolution_per_User': input_data['Resolution_per_User'],
            'Attack_Defense': input_data['Attack_Defense'],
            'Industry_Vulnerability': input_data['Industry_Vulnerability'],
            'Time_Factor': input_data['Time_Factor']
        }
        
        # Ajouter les moyennes par catégorie
        df_data['Avg_Loss_by_Attack'] = loss_mappings['attack'][input_data[ATTACK_TYPE]]
        df_data['Avg_Loss_by_Industry'] = loss_mappings['industry'][input_data[TARGET_INDUSTRY]]
        df_data['Avg_Loss_by_Vulnerability'] = loss_mappings['vulnerability'][input_data[VULNERABILITY_TYPE]]
        
        # Créer le DataFrame
        input_df = pd.DataFrame([df_data])
        
        # Normaliser les features numériques
        numerical_features = [AFFECTED_USERS, RESOLUTION_TIME, 
                            'Avg_Loss_by_Attack', 'Avg_Loss_by_Industry', 'Avg_Loss_by_Vulnerability']
        input_df[numerical_features] = scaler.transform(input_df[numerical_features])
        
        # S'assurer que les colonnes sont dans le bon ordre sans noms
        X = input_df[selected_features].values
        
        # Faire la prédiction
        prediction = model.predict(X)[0]
        tree_predictions = np.array([tree.predict(X)[0] for tree in model.estimators_])
        confidence_interval = np.percentile(tree_predictions, [5, 95])
        
        return {
            'prediction': f"{prediction:.2f}",
            'confidence_low': f"{confidence_interval[0]:.2f}",
            'confidence_high': f"{confidence_interval[1]:.2f}"
        }
    except Exception as e:
        print("Erreur dans make_prediction:")
        print("Données d'entrée:", input_data)
        print("Features attendues:", selected_features)
        print("Features disponibles:", list(input_df.columns))
        raise ValueError(f"Erreur lors de la prédiction: {str(e)}")














@app.route('/prediction', methods=['GET', 'POST'])
def prediction():
    prediction_result = None
    categories = {}
    
    try:
        # Charger le modèle
        model_info = joblib.load('loss_per_user_model.joblib')
        print("Modèle chargé avec succès")
        print("Features du modèle:", model_info['selected_features'])
        
        # Préparer les catégories
        for form_field, encoder_key in FIELD_TO_ENCODER.items():
            categories[form_field + 's'] = sorted(model_info['encoders'][encoder_key].classes_.tolist())
        
        if request.method == 'POST':
            try:
                print("Données du formulaire reçues:", request.form)
                # Valider les entrées numériques
                affected_users, resolution_time, current_year = validate_numeric_input(request.form)
                
                # Préparer les données
                input_data = prepare_prediction_data(
                    request.form, 
                    model_info['encoders'],
                    affected_users,
                    resolution_time,
                    current_year
                )
                print("Données préparées:", input_data)
                
                # Faire la prédiction
                prediction_result = make_prediction(
                    input_data,
                    model_info['model'],
                    model_info['scaler'],
                    model_info['selected_features'],
                    model_info['loss_per_user_mappings']
                )
                print("Prédiction réussie:", prediction_result)
                
            except ValueError as e:
                print(f"Erreur de validation: {str(e)}")
                prediction_result = {'error': str(e)}
            except Exception as e:
                print(f"Erreur inattendue: {str(e)}")
                prediction_result = {'error': f"Erreur inattendue: {str(e)}"}
    
    except Exception as e:
        print(f"Erreur de chargement du modèle: {str(e)}")
        prediction_result = {'error': f"Erreur lors du chargement du modèle: {str(e)}"}
    
    return render_template('prediction.html', 
                         prediction_result=prediction_result,
                         categories=categories)

if __name__ == '__main__':
>>>>>>> 05238f3a83981a3c4a40aa1103d176ca2d031b9c
    app.run(debug=True)