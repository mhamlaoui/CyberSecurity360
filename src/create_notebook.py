import nbformat as nbf

nb = nbf.v4.new_notebook()

# Cellule 1 - Markdown d'introduction
nb['cells'] = [nbf.v4.new_markdown_cell('''# Modèle de Prédiction des Pertes par Utilisateur

Ce notebook contient le modèle qui prédit les pertes financières par utilisateur lors d'une cyberattaque.

## 1. Import des bibliothèques''')]

# Cellule 2 - Imports
nb['cells'].append(nbf.v4.new_code_cell('''import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import joblib'''))

# Cellule 3 - Markdown pour le chargement des données
nb['cells'].append(nbf.v4.new_markdown_cell('''## 2. Chargement des données'''))

# Cellule 4 - Chargement des données
nb['cells'].append(nbf.v4.new_code_cell('''print("📂 Chargement des données...")
data = pd.read_csv('kaggle_data.csv')
print(f"Données chargées: {data.shape[0]} lignes, {data.shape[1]} colonnes\\n")'''))

# Cellule 5 - Markdown pour le feature engineering
nb['cells'].append(nbf.v4.new_markdown_cell('''## 3. Feature Engineering

### 3.1 Calcul de la variable cible'''))

# Cellule 6 - Calcul des pertes par utilisateur
nb['cells'].append(nbf.v4.new_code_cell('''# Calcul des pertes par utilisateur
data['Loss_per_User'] = (data['Financial Loss (in Million $)'] * 1_000_000) / data['Number of Affected Users']
print(f"Pertes moyennes par utilisateur: {data['Loss_per_User'].mean():.2f} $")'''))

# Cellule 7 - Markdown pour l'encodage
nb['cells'].append(nbf.v4.new_markdown_cell('''### 3.2 Encodage des variables catégorielles'''))

# Cellule 8 - Encodage
nb['cells'].append(nbf.v4.new_code_cell('''# Encodage des variables catégorielles
encoders = {}
categorical_features = ['Attack Type', 'Target Industry', 'Attack Source', 
                       'Security Vulnerability Type', 'Defense Mechanism Used']
for feature in categorical_features:
    encoders[feature] = LabelEncoder()
    data[feature] = encoders[feature].fit_transform(data[feature])'''))

# Cellule 9 - Markdown pour les features agrégées
nb['cells'].append(nbf.v4.new_markdown_cell('''### 3.3 Création des features agrégées'''))

# Cellule 10 - Features agrégées
nb['cells'].append(nbf.v4.new_code_cell('''# Calcul des moyennes par groupe
loss_per_user_by_attack = data.groupby('Attack Type')['Loss_per_User'].mean()
loss_per_user_by_industry = data.groupby('Target Industry')['Loss_per_User'].mean()
loss_per_user_by_vulnerability = data.groupby('Security Vulnerability Type')['Loss_per_User'].mean()

# Création des features de moyenne
data['Avg_Loss_by_Attack'] = data['Attack Type'].map(loss_per_user_by_attack)
data['Avg_Loss_by_Industry'] = data['Target Industry'].map(loss_per_user_by_industry)
data['Avg_Loss_by_Vulnerability'] = data['Security Vulnerability Type'].map(loss_per_user_by_vulnerability)'''))

# Cellule 11 - Markdown pour la normalisation
nb['cells'].append(nbf.v4.new_markdown_cell('''### 3.4 Normalisation des features numériques'''))

# Cellule 12 - Normalisation
nb['cells'].append(nbf.v4.new_code_cell('''# Features numériques
numerical_features = ['Number of Affected Users', 'Incident Resolution Time (in Hours)',
                     'Avg_Loss_by_Attack', 'Avg_Loss_by_Industry', 'Avg_Loss_by_Vulnerability']

# Normalisation
scaler = StandardScaler()
data[numerical_features] = scaler.fit_transform(data[numerical_features])'''))

# Cellule 13 - Markdown pour les features d'interaction
nb['cells'].append(nbf.v4.new_markdown_cell('''### 3.5 Création des features d'interaction'''))

# Cellule 14 - Features d'interaction
nb['cells'].append(nbf.v4.new_code_cell('''# Features d'interaction
data['Resolution_per_User'] = data['Incident Resolution Time (in Hours)'] / data['Number of Affected Users']
data['Attack_Defense'] = data['Attack Type'] * data['Defense Mechanism Used']
data['Industry_Vulnerability'] = data['Target Industry'] * data['Security Vulnerability Type']
data['Time_Factor'] = (2024 - data['Year']) / 10'''))

# Cellule 15 - Markdown pour la préparation des données
nb['cells'].append(nbf.v4.new_markdown_cell('''## 4. Préparation des données pour l'entraînement'''))

# Cellule 16 - Préparation des données
nb['cells'].append(nbf.v4.new_code_cell('''# Sélection des features
selected_features = (numerical_features + categorical_features + 
                    ['Resolution_per_User', 'Attack_Defense', 'Industry_Vulnerability', 'Time_Factor'])

# Préparation des données
X = data[selected_features]
y = data['Loss_per_User']

# Split des données
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)'''))

# Cellule 17 - Markdown pour l'entraînement
nb['cells'].append(nbf.v4.new_markdown_cell('''## 5. Entraînement du modèle'''))

# Cellule 18 - Entraînement
nb['cells'].append(nbf.v4.new_code_cell('''print("🤖 Entraînement du modèle...")
model = RandomForestRegressor(
    n_estimators=300,
    max_depth=12,
    min_samples_split=5,
    min_samples_leaf=2,
    max_features='sqrt',
    bootstrap=True,
    random_state=42,
    n_jobs=-1
)

# Validation croisée
print("\\n📊 Validation croisée...")
cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='r2')
print(f"Scores R² (validation croisée): {cv_scores.mean():.3f} (±{cv_scores.std()*2:.3f})")

# Entraînement final
model.fit(X_train, y_train)'''))

# Cellule 19 - Markdown pour l'évaluation
nb['cells'].append(nbf.v4.new_markdown_cell('''## 6. Évaluation du modèle'''))

# Cellule 20 - Évaluation
nb['cells'].append(nbf.v4.new_code_cell('''# Évaluation
print("\\n📈 Évaluation du modèle...")
y_pred = model.predict(X_test)

rmse = np.sqrt(mean_squared_error(y_test, y_pred))
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("\\nMétriques de performance:")
print(f"RMSE: {rmse:.2f} $ par utilisateur")
print(f"MAE: {mae:.2f} $ par utilisateur")
print(f"R²: {r2:.3f}")'''))

# Cellule 21 - Markdown pour l'analyse des features
nb['cells'].append(nbf.v4.new_markdown_cell('''## 7. Analyse des features importantes'''))

# Cellule 22 - Importance des features
nb['cells'].append(nbf.v4.new_code_cell('''# Importance des features
feature_importance = pd.DataFrame({
    'feature': selected_features,
    'importance': model.feature_importances_
})
feature_importance = feature_importance.sort_values('importance', ascending=False)
print("\\n🔍 Top 10 features les plus importantes:")
print(feature_importance.head(10))'''))

# Cellule 23 - Markdown pour le test
nb['cells'].append(nbf.v4.new_markdown_cell('''## 8. Test de prédiction'''))

# Cellule 24 - Test de prédiction
nb['cells'].append(nbf.v4.new_code_cell('''# Test de prédiction
print("\\n💡 Test de prédiction...")
example = X_test.iloc[0].copy()
prediction = model.predict([example])[0]

# Calcul de l'intervalle de confiance
tree_predictions = np.array([tree.predict([example])[0] 
                           for tree in model.estimators_])
confidence_interval = np.percentile(tree_predictions, [5, 95])

print(f"\\n💰 Perte par utilisateur prédite: {prediction:.2f} $")
print(f"Intervalle de confiance (90%): [{confidence_interval[0]:.2f}, {confidence_interval[1]:.2f}] $")'''))

# Cellule 25 - Markdown pour la sauvegarde
nb['cells'].append(nbf.v4.new_markdown_cell('''## 9. Sauvegarde du modèle'''))

# Cellule 26 - Sauvegarde
nb['cells'].append(nbf.v4.new_code_cell('''# Sauvegarde du modèle
print("\\n💾 Sauvegarde du modèle...")
model_info = {
    'model': model,
    'encoders': encoders,
    'scaler': scaler,
    'selected_features': selected_features,
    'loss_per_user_mappings': {
        'attack': loss_per_user_by_attack,
        'industry': loss_per_user_by_industry,
        'vulnerability': loss_per_user_by_vulnerability
    },
    'feature_importance': feature_importance.to_dict(),
    'metrics': {
        'rmse': rmse,
        'mae': mae,
        'r2': r2,
        'cv_scores': {
            'mean': cv_scores.mean(),
            'std': cv_scores.std()
        }
    }
}
joblib.dump(model_info, 'loss_per_user_model.joblib')
print("✅ Modèle sauvegardé!")'''))

# Sauvegarde du notebook
with open('model.ipynb', 'w', encoding='utf-8') as f:
    nbf.write(nb, f) 