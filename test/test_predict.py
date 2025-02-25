import pytest
from src.model_pipeline import load_model, predict
import numpy as np

def test_predict():
    # Charger le modèle
    model = load_model()
    
    # Vérifier que le modèle a bien été chargé
    assert model is not None, "Le modèle n'a pas été chargé"
    
    # Créer des données factices pour la prédiction (20 caractéristiques, car X_train a 20 colonnes dans votre projet)
    sample_features = np.random.rand(1, 20)
    
    # Faire une prédiction
    prediction = predict(sample_features, model=model)
    
    # Vérifier que la prédiction est valide (0 ou 1)
    assert prediction in [0, 1], f"La prédiction {prediction} n'est pas valide"
