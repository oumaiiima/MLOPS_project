import argparse
import numpy as np
import mlflow
import mlflow.sklearn
from model_pipeline import (
    prepare_data,
    train_model,
    save_model,
    load_model,
    evaluate_model,
    predict,
)


def prepare_only(train_path, test_path):
    """
    Prepare the data without training the model.
    """
    X_train, X_test, y_train, y_test = prepare_data(train_path, test_path)
    print("\n✅ Data Preparation Completed!")
    print(f"📊 X_train shape: {X_train.shape}")
    print(f"📊 X_test shape: {X_test.shape}")


def assign_stage_to_model_version(model_name, version, stage):
    """
    Assign a stage to a specific model version.
    """
    try:
        client = mlflow.tracking.MlflowClient()
        client.transition_model_version_stage(
            name=model_name, version=version, stage=stage
        )
        print(
            f"✅ Version {version} du modèle '{model_name}' assignée au stage '{stage}'."
        )
    except Exception as e:
        print(f"❌ Failed to assign stage: {e}")


def main(
    train_path=None,
    test_path=None,
    prepare_only_flag=False,
    predict_flag=False,
    mlflow_flag=False,
    register_flag=False,
    evaluate_flag=False,
    stage=None,
    model_version=None,
    assign_stage=None,
):
    """
    Main function to handle data preparation, training, evaluation, and prediction.
    """
    # Configurer le Tracking URI
    mlflow.set_tracking_uri("http://localhost:5000")
    print(f"Tracking URI: {mlflow.get_tracking_uri()}")

    # Assigner un stage à une version si demandé
    if assign_stage:
        if not model_version:
            raise ValueError(
                "❌ Vous devez spécifier une version avec --model_version pour assigner un stage."
            )
        assign_stage_to_model_version(
            "Churn_Prediction_Model", model_version, assign_stage
        )
        return

    if predict_flag:
        print("\n🎯 Running Prediction Mode...")

        # Charger le modèle de MLflow Model Registry
        if stage and model_version:
            raise ValueError(
                "❌ Vous ne pouvez pas spécifier à la fois un stage et une version. Utilisez l'un ou l'autre."
            )
        elif stage:
            model_uri = f"models:/Churn_Prediction_Model@{stage}"  # Charger par stage
        elif model_version:
            model_uri = (
                f"models:/Churn_Prediction_Model/{model_version}"  # Charger par version
            )
        else:
            raise ValueError(
                "❌ Vous devez spécifier soit un stage, soit une version pour charger le modèle."
            )

        print(f"📥 Loading model from: {model_uri}")

        try:
            loaded_model = mlflow.sklearn.load_model(model_uri)
            print("✅ Model loaded successfully!")
        except Exception as e:
            print(f"❌ Failed to load model: {e}")
            return

        # Simuler des fonctionnalités d'exemple pour la prédiction
        sample_features = np.random.rand(
            1, 20
        )  # Ajustez les dimensions en fonction des données d'entraînement (20 colonnes)

        # Faire une prédiction
        prediction = predict(sample_features, model=loaded_model)
        print(f"\n🎯 Prediction Result: {prediction}")

    elif prepare_only_flag:
        if train_path is None or test_path is None:
            raise ValueError(
                "❌ Les arguments --train et --test sont requis pour la préparation des données."
            )
        prepare_only(train_path, test_path)
    elif evaluate_flag:
        if train_path is None or test_path is None:
            raise ValueError(
                "❌ Les arguments --train et --test sont requis pour l'évaluation du modèle."
            )

        # Préparation des données
        X_train, X_test, y_train, y_test = prepare_data(train_path, test_path)
        print("\n✅ Data Preparation Completed!")

        # Charger le modèle
        model = load_model("gbm_model.joblib")
        print("\n📥 Model loaded successfully!")

        # Évaluation du modèle
        print("\n📊 Evaluating the model...")
        evaluate_model(model, X_test, y_test)
        print("✅ Model evaluation successful!")
    else:
        if train_path is None or test_path is None:
            raise ValueError(
                "❌ Les arguments --train et --test sont requis pour l'entraînement du modèle."
            )

        # Préparation des données
        X_train, X_test, y_train, y_test = prepare_data(train_path, test_path)
        print("\n✅ Data Preparation Completed!")

        print("\n🚀 Training Model...")
        model = train_model(X_train, y_train, mlflow_flag=mlflow_flag)

        # Sauvegarde du modèle localement
        save_model(model)
        print("\n✅ Model saved successfully!")

        # Enregistrement dans le registre MLflow si nécessaire
        if mlflow_flag and register_flag:
            mlflow.sklearn.log_model(model, "Churn_Prediction_Model")
            print("\n✅ Modèle enregistré dans MLflow Model Registry !")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Train, evaluate, or predict using the model pipeline."
    )
    parser.add_argument(
        "--train", type=str, required=False, help="Path to the training CSV file"
    )
    parser.add_argument(
        "--test", type=str, required=False, help="Path to the test CSV file"
    )
    parser.add_argument(
        "--prepare",
        action="store_true",
        help="Only prepare the data, don't train the model",
    )
    parser.add_argument(
        "--predict", action="store_true", help="Run a prediction using a trained model"
    )
    parser.add_argument(
        "--mlflow",
        action="store_true",
        help="Enable MLflow tracking for model training",
    )
    parser.add_argument(
        "--register",
        action="store_true",
        help="Register the trained model in MLflow Model Registry",
    )
    parser.add_argument(
        "--evaluate", action="store_true", help="Evaluate the trained model"
    )
    parser.add_argument(
        "--stage", type=str, help="Stage of the model (e.g., 'Production', 'Staging')"
    )
    parser.add_argument(
        "--model_version",
        type=int,
        default=None,
        help="Version of the model in MLflow Model Registry",
    )
    parser.add_argument(
        "--assign_stage",
        type=str,
        help="Assign a stage (e.g., 'Production', 'Staging') to a model version",
    )

    args = parser.parse_args()

    main(
        args.train,
        args.test,
        prepare_only_flag=args.prepare,
        predict_flag=args.predict,
        mlflow_flag=args.mlflow,
        register_flag=args.register,
        evaluate_flag=args.evaluate,
        stage=args.stage,
        model_version=args.model_version,
        assign_stage=args.assign_stage,
    )
