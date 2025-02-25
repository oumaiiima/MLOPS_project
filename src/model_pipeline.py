import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import randint, uniform
import joblib
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import mlflow
import mlflow.sklearn


def prepare_data(train_path, test_path):
    """
    Prépare les données en les chargeant, en les nettoyant et en les divisant en ensembles d'entraînement et de test.
    """
    try:
        df_train = pd.read_csv(train_path)
        df_test = pd.read_csv(test_path)
        df = pd.concat([df_train, df_test], axis=0, ignore_index=True)

        # Encodage des variables catégorielles
        df["International plan"] = df["International plan"].map({"Yes": 1, "No": 0})
        df["Voice mail plan"] = df["Voice mail plan"].map({"Yes": 1, "No": 0})
        df["Churn"] = df["Churn"].astype(int)

        # Encodage de la variable "State"
        target_mean = df.groupby("State")["Churn"].mean()
        df["STATE_TargetMean"] = df["State"].map(target_mean)

        label_encoder = LabelEncoder()
        df["STATE_Label"] = label_encoder.fit_transform(df["State"])
        df = df.drop(columns=["State"])

        # Séparation des features et de la cible
        X = df.drop(columns=["Churn"])
        y = df["Churn"]

        # Rééquilibrage des classes avec SMOTE
        smote = SMOTE(random_state=42)
        X, y = smote.fit_resample(X, y)

        # Division en ensembles d'entraînement et de test
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Normalisation des données
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        return X_train_scaled, X_test_scaled, y_train, y_test

    except Exception as e:
        print(f"❌ Erreur lors de la préparation des données : {e}")
        return None, None, None, None


def train_model(X_train, y_train, mlflow_flag=False):
    """
    Entraîne un modèle Gradient Boosting Classifier avec une recherche aléatoire d'hyperparamètres.
    """
    try:
        if mlflow_flag:
            # Configuration de MLflow
            mlflow.set_tracking_uri("http://localhost:5000")

            # Définir l'expérience "Churn_Prediction"
            experiment_name = "Churn_Prediction"
            if not mlflow.get_experiment_by_name(experiment_name):
                mlflow.create_experiment(experiment_name)
            mlflow.set_experiment(experiment_name)

        # Distribution des hyperparamètres pour la recherche aléatoire
        param_dist = {
            "n_estimators": randint(50, 200),
            "learning_rate": uniform(0.01, 0.2),
            "max_depth": [3, 5, 7],
            "subsample": [0.8, 1.0],
        }

        # Initialisation du modèle
        gb_model = GradientBoostingClassifier(random_state=42)
        random_search = RandomizedSearchCV(
            gb_model,
            param_distributions=param_dist,
            n_iter=20,
            cv=3,
            scoring="accuracy",
            verbose=1,
            n_jobs=-1,
        )

        # Recherche des meilleurs hyperparamètres
        random_search.fit(X_train, y_train)
        best_model = random_search.best_estimator_

        if mlflow_flag:
            # Enregistrement des résultats dans MLflow
            with mlflow.start_run():
                mlflow.log_params(random_search.best_params_)
                mlflow.log_metric("accuracy", random_search.best_score_)
                model_info = mlflow.sklearn.log_model(best_model, "Churn_Prediction_Model")
                mlflow.register_model(
                    model_uri=model_info.model_uri, name="Churn_Prediction_Model"
                )

        return best_model

    except Exception as e:
        print(f"❌ Erreur lors de l'entraînement du modèle : {e}")
        return None


def evaluate_model(model, X_test, y_test):
    """
    Évalue le modèle sur les données de test et retourne l'accuracy et le rapport de classification.
    """
    try:
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred)
        cm = confusion_matrix(y_test, y_pred)

        # Affichage de la matrice de confusion
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
        plt.title("Confusion Matrix")
        plt.xlabel("Predicted")
        plt.ylabel("Actual")
        plt.show()

        print(f"\n✅ Evaluation Completed!")
        print(f"📊 Accuracy: {accuracy:.4f}")
        print(f"📊 Classification Report:\n{report}")

        return accuracy, report  # Retourner les valeurs

    except Exception as e:
        print(f"❌ Erreur lors de l'évaluation du modèle : {e}")
        return None, None  # Retourner None en cas d'erreur


def save_model(model, filename="gbm_model.joblib"):
    """
    Sauvegarde le modèle entraîné dans un fichier.
    """
    try:
        joblib.dump(model, filename)
        print(f"\n💾 Model saved to '{filename}'")
    except Exception as e:
        print(f"❌ Erreur lors de la sauvegarde du modèle : {e}")


def load_model(filename="gbm_model.joblib"):
    """
    Charge un modèle à partir d'un fichier.
    """
    try:
        model = joblib.load(filename)
        print(f"\n📂 Model loaded from '{filename}'")
        return model
    except Exception as e:
        print(f"❌ Erreur lors du chargement du modèle : {e}")
        return None


def predict(features, model=None, filename="gbm_model.joblib"):
    """
    Effectue une prédiction à partir des features fournies.
    """
    try:
        if model is None:
            model = joblib.load(filename)
        prediction = model.predict(features)
        print(f"\n✅ Prediction Completed! Prediction: {prediction}")
        return prediction
    except Exception as e:
        print(f"❌ Erreur lors de la prédiction : {e}")
        return None