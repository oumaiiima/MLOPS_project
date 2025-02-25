import pytest
from src.model_pipeline import evaluate_model
from sklearn.ensemble import GradientBoostingClassifier
import numpy as np


def test_evaluate_model():
    # Créer des données factices pour l'entraînement et le test
    X_train = np.random.rand(
        100, 20
    )  # 100 échantillons, 20 caractéristiques (car X_train a 20 colonnes dans votre projet)
    y_train = np.random.randint(0, 2, 100)  # Labels binaires (0 ou 1)
    X_test = np.random.rand(50, 20)  # 50 échantillons, 20 caractéristiques
    y_test = np.random.randint(0, 2, 50)  # Labels binaires (0 ou 1)

    # Entraîner le modèle
    model = GradientBoostingClassifier(random_state=42)
    model.fit(X_train, y_train)

    # Évaluer le modèle (vérifier qu'il n'y a pas d'erreur)
    evaluate_model(model, X_test, y_test)
