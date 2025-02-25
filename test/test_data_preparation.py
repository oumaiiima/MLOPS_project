import pytest
from src.model_pipeline import prepare_data

def test_prepare_data():
    # Appeler la fonction prepare_data avec les chemins des fichiers de données
    X_train, X_test, y_train, y_test = prepare_data("data/train.csv", "data/test.csv")
    
    # Vérifier que les données préparées ne sont pas vides
    assert X_train.shape[0] > 0, "X_train ne doit pas être vide"
    assert X_test.shape[0] > 0, "X_test ne doit pas être vide"
    assert len(y_train) > 0, "y_train ne doit pas être vide"
    assert len(y_test) > 0, "y_test ne doit pas être vide"