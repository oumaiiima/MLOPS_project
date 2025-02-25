import time
import pytest
from src.model_pipeline import prepare_data, train_model

def test_training_time():
    # Préparer les données
    X_train, _, y_train, _ = prepare_data("data/train.csv", "data/test.csv")
    
    # Vérifier que les données préparées ne sont pas vides
    assert X_train.shape[0] > 0, "X_train ne doit pas être vide"
    assert len(y_train) > 0, "y_train ne doit pas être vide"
    
    # Mesurer le temps d'entraînement
    start_time = time.time()
    train_model(X_train, y_train)
    training_time = time.time() - start_time
    
    # Vérifier que l'entraînement prend moins de 60 secondes
    assert training_time < 60, f"L'entraînement a pris trop de temps : {training_time:.2f} secondes"
