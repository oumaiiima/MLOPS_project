import pytest
from src.model_pipeline import train_model
import numpy as np


def test_train_model():
    # Créer des données factices pour l'entraînement
    X_train = np.random.rand(
        100, 20
    )  # 100 échantillons, 20 caractéristiques (car X_train a 20 colonnes dans votre projet)
    y_train = np.random.randint(0, 2, 100)  # Labels binaires (0 ou 1)

    # Entraîner le modèle
    model = train_model(X_train, y_train)

    # Vérifier que le modèle a bien été entraîné
    assert model is not None, "Le modèle n'a pas été entraîné"
