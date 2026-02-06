import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import joblib

print("📂 Chargement des données...")
data = pd.read_csv('kaggle_data.csv')
print(f"Données chargées: {data.shape[0]} lignes, {data.shape[1]} colonnes\n")

print("🛠️ Feature engineering...")
# Calcul de la variable cible : pertes par utilisateur
data['Loss_per_User'] = (data['Financial Loss (in Million $)'] * 1_000_000) / data['Number of Affected Users']
print(f"Pertes moyennes par utilisateur: {data['Loss_per_User'].mean():.2f} $")

# Encodage des variables catégorielles
encoders = {}
categorical_features = ['Attack Type', 'Target Industry', 'Attack Source', 
                       'Security Vulnerability Type', 'Defense Mechanism Used']
for feature in categorical_features:
    encoders[feature] = LabelEncoder()
    data[feature] = encoders[feature].fit_transform(data[feature])

# Calcul des moyennes par groupe
loss_per_user_by_attack = data.groupby('Attack Type')['Loss_per_User'].mean()
loss_per_user_by_industry = data.groupby('Target Industry')['Loss_per_User'].mean()
loss_per_user_by_vulnerability = data.groupby('Security Vulnerability Type')['Loss_per_User'].mean()

# Création des features de moyenne
data['Avg_Loss_by_Attack'] = data['Attack Type'].map(loss_per_user_by_attack)
data['Avg_Loss_by_Industry'] = data['Target Industry'].map(loss_per_user_by_industry)
data['Avg_Loss_by_Vulnerability'] = data['Security Vulnerability Type'].map(loss_per_user_by_vulnerability)

# Features numériques
numerical_features = ['Number of Affected Users', 'Incident Resolution Time (in Hours)',
                     'Avg_Loss_by_Attack', 'Avg_Loss_by_Industry', 'Avg_Loss_by_Vulnerability']

# Normalisation des variables numériques
scaler = StandardScaler()
data[numerical_features] = scaler.fit_transform(data[numerical_features])

# Création de features d'interaction
data['Resolution_per_User'] = data['Incident Resolution Time (in Hours)'] / data['Number of Affected Users']
data['Attack_Defense'] = data['Attack Type'] * data['Defense Mechanism Used']
data['Industry_Vulnerability'] = data['Target Industry'] * data['Security Vulnerability Type']
data['Time_Factor'] = (2024 - data['Year']) / 10

# Sauvegarde des données transformées
print("\n💾 Sauvegarde des données transformées...")
# Créer un dictionnaire pour stocker les noms originaux des catégories
original_names = {}
for feature in categorical_features:
    original_names[feature] = dict(zip(encoders[feature].transform(encoders[feature].classes_), 
                                     encoders[feature].classes_))
    # Reconvertir les valeurs encodées en noms originaux
    data[feature] = data[feature].map(original_names[feature])

# Sélectionner toutes les colonnes pertinentes
columns_to_save = (
    categorical_features + 
    ['Year', 'Number of Affected Users', 'Incident Resolution Time (in Hours)', 
     'Financial Loss (in Million $)', 'Loss_per_User',
     'Avg_Loss_by_Attack', 'Avg_Loss_by_Industry', 'Avg_Loss_by_Vulnerability',
     'Resolution_per_User', 'Attack_Defense', 'Industry_Vulnerability', 'Time_Factor']
)

# Sauvegarder en CSV
data[columns_to_save].to_csv('transformed_data.csv', index=False)
print("✅ Données transformées sauvegardées dans transformed_data.csv")

# Ré-encoder les variables catégorielles pour l'entraînement
for feature in categorical_features:
    data[feature] = encoders[feature].transform(data[feature])

# Sélection des features pour le modèle
selected_features = (numerical_features + categorical_features + 
                    ['Resolution_per_User', 'Attack_Defense', 'Industry_Vulnerability', 'Time_Factor'])

# Préparation des données
X = data[selected_features]
y = data['Loss_per_User']

# Split des données
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("\n🤖 Entraînement du modèle...")
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
print("\n📊 Validation croisée...")
cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='r2')
print(f"Scores R² (validation croisée): {cv_scores.mean():.3f} (±{cv_scores.std()*2:.3f})")

# Entraînement final
model.fit(X_train, y_train)

# Évaluation
print("\n📈 Évaluation du modèle...")
y_pred = model.predict(X_test)

rmse = np.sqrt(mean_squared_error(y_test, y_pred))
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("\nMétriques de performance:")
print(f"RMSE: {rmse:.2f} $ par utilisateur")
print(f"MAE: {mae:.2f} $ par utilisateur")
print(f"R²: {r2:.3f}")

# Importance des features
feature_importance = pd.DataFrame({
    'feature': selected_features,
    'importance': model.feature_importances_
})
feature_importance = feature_importance.sort_values('importance', ascending=False)
print("\n🔍 Top 10 features les plus importantes:")
print(feature_importance.head(10))

# Test de prédiction
print("\n💡 Test de prédiction...")
example = X_test.iloc[0].copy()
prediction = model.predict([example])[0]

# Calcul de l'intervalle de confiance
tree_predictions = np.array([tree.predict([example])[0] 
                           for tree in model.estimators_])
confidence_interval = np.percentile(tree_predictions, [5, 95])

print(f"\n💰 Perte par utilisateur prédite: {prediction:.2f} $")
print(f"Intervalle de confiance (90%): [{confidence_interval[0]:.2f}, {confidence_interval[1]:.2f}] $")

# Sauvegarde du modèle
print("\n💾 Sauvegarde du modèle...")
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
print("✅ Modèle sauvegardé!") 