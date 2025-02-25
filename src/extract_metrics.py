import mlflow
import json

# Configurer le Tracking URI
mlflow.set_tracking_uri("http://localhost:5000")


def extract_latest_metrics():
    """
    Extrait les métriques de la dernière run MLflow et les sauvegarde dans un fichier JSON.
    """
    try:
        # Récupérer la dernière run
        runs = mlflow.search_runs(order_by=["start_time DESC"], max_results=1)
        if runs.empty:
            print("Aucune run trouvée dans MLflow.")
            # Créer un fichier JSON vide
            with open("mlflow_metrics.json", "w") as f:
                json.dump({}, f)
            return

        latest_run = runs.iloc[0]

        # Extraire les métriques
        metrics = {
            "run_id": latest_run["run_id"],
            "accuracy": latest_run.get("metrics.accuracy", "N/A"),
            "precision": latest_run.get("metrics.precision", "N/A"),
            "recall": latest_run.get("metrics.recall", "N/A"),
            "f1_score": latest_run.get("metrics.f1_score", "N/A"),
        }

        # Sauvegarder les métriques dans un fichier JSON
        with open("mlflow_metrics.json", "w") as f:
            json.dump(metrics, f, indent=4)

        print("Métriques extraites avec succès :", metrics)
    except Exception as e:
        print(f"❌ Erreur lors de l'extraction des métriques : {e}")
        # Créer un fichier JSON vide en cas d'erreur
        with open("mlflow_metrics.json", "w") as f:
            json.dump({}, f)


if __name__ == "__main__":
    extract_latest_metrics()
    extract_latest_metrics()