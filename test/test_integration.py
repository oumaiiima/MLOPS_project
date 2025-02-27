import pytest
from src.model_pipeline import prepare_data, train_model, evaluate_model


def test_pipeline():
    # Préparer les données
    X_train, X_test, y_train, y_test = prepare_data("data/train.csv", "data/test.csv")

    # Vérifier que les données préparées ne sont pas vides
    assert X_train.shape[0] > 0, "X_train ne doit pas être vide"
    assert X_test.shape[0] > 0, "X_test ne doit pas être vide"
    assert len(y_train) > 0, "y_train ne doit pas être vide"
    assert len(y_test) > 0, "y_test ne doit pas être vide"

    # Entraîner le modèle
    model = train_model(X_train, y_train)

    # Vérifier que le modèle a bien été entraîné
    assert model is not None, "Le modèle n'a pas été entraîné"

    # Évaluer le modèle (vérifier qu'il n'y a pas d'erreur)
    evaluate_model(model, X_test, y_test)
