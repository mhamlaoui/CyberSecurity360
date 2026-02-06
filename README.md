# Cybersécurité 360

##  Table des matières
- [Contexte du projet](#contexte-du-projet)
- [Objectifs](#objectifs)
- [MVP](#mvp)
- [Backlog](#backlog)
- [Technologies utilisées](#technologies-utilisées)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Captures d'écran](#captures-décran)
- [Membres du projet](#membres-du-projet)

##  Contexte du projet

Dans un monde où les cyberattaques deviennent de plus en plus fréquentes et sophistiquées, il est nécessaire d'avoir une vision claire des menaces informatiques. Notre projet vise à créer une plateforme de visualisation interactive qui permet de comprendre et d'analyser les tendances des cyberattaques à l'échelle mondiale, donnant aux entreprises un moyen de prioriser leur points faibles à renforcer. Notre solution est également accompagné d'un chat bot alimenté par l'Intelligence Artificielle, permettant à l'utilisateur d'avoir une réponse à ses questions en rapport avec la cybersécurité

##  Objectifs

- Créer une carte interactive mondiale des cyberattaques
- Fournir des analyses détaillées des différents types d'attaques
- Permettre le filtrage des données par date, type d'attaque et localisation
- Intégrer un chatbot explicatif sur les types d'attaques
- Offrir des visualisations de données sous forme de graphiques et tableaux
- Assurer une documentation complète des données sources

##  MVP (Minimum Viable Product)

Notre MVP comprend les fonctionnalités essentielles suivantes :
- Carte interactive mondiale avec visualisation des attaques
- Système de filtrage basique (date, type d'attaque)
- Interface utilisateur intuitive et responsive
- Visualisation des données en temps réel
- Documentation des sources de données


##  Technologies utilisées

- **Frontend** : 
    - Html
    - Css
    - Js


- **Backend** : 
  - Python
  - Pandas 
  - Llama_cpp
  - Os

- **Déploiement** : 
  - Flask

- **Outils d'analyse** : 
  - Power BI 
  - Jupyter Notebooks

## 🛠️ Installation

1. Cloner le repository
```bash
git clone https://github.com/votre-username/cybersecurite-360.git
cd cybersecurite-360
```

2. Installer les dépendances Python
```bash
pip install -r requirements.txt
```

3. Télécharger le modèle Llama
Le modèle Llama n'est pas inclus dans le dépôt Git en raison de sa taille. Vous devez le télécharger séparément :
- Créez un dossier `src/models` s'il n'existe pas
- Téléchargez le modèle `Llama-3.2-1B-Instruct-Q4_0.gguf` depuis le lien suivant : https://huggingface.co/bartowski/Llama-3.2-1B-Instruct-GGUF/blob/main/Llama-3.2-1B-Instruct-Q4_0.gguf
- Placez le fichier dans le dossier `src/models`

4. Lancer l'application
```bash
python app.py
```

##  Utilisation

Pour accéder à l'application, lancez le serveur et ouvrez `http://localhost:5000` dans votre navigateur.

Notre application se compose de cinq sections principales :

### Tableau de bord
Visualisez les cyberattaques sur une carte interactive mondiale. Utilisez les filtres pour rechercher des attaques spécifiques par date, type ou région.

### Modèle prédictif
-- Préditctions à rajouter -- .

### Assistant IA
Posez vos questions sur la cybersécurité à notre assistant IA. Il vous fournira des explications détaillées sur les types d'attaques et les bonnes pratiques de sécurité.

### Informations
Retrouvez des informations sur notre projet, en particulier les types d'attaques que nous traitons et l'explication des données que nous utilisons.

### Contact
Contactez-nous pour toute question ou nous laisser un avis.


## 📸 Captures d'écran

### Interface principale
![Interface principale](src/static/images/screenshots/index_readme.jpeg)

### Carte interactive
![Carte interactive](src/static/images/screenshots/map-view.png)

### Tableau de bord
![Tableau de bord](src/static/images/screenshots/dashboard_readme.jpeg)

### Chatbot
![Chatbot](src/static/images/screenshots/chatbot_readme.jpeg)

### Informations
![Informations](src/static/images/screenshots/informations_readme.jpeg)

### Prédictions
![Prédictions](src/static/images/screenshots/predictions_readme.jpeg)

##  Membres du projet

- **Ilhan Gokmen** 
- **Mohamed Ilias Hamlaoui**
- **Louisa Ould Bouali**
- **Oussama Yassine**
- **Melissa Yessad**
