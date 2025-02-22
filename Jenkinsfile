pipeline {
    agent any
    environment {
        GIT_TOKEN = credentials('token-oum')  // Utilise l'ID de l'identifiant GitHub
    }
    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/oumaiiima/MLOPS_project.git', credentialsId: 'github-token'
            }
        }
        stage('Install Dependencies') {
            steps {
                script {
                    // Installe les dépendances nécessaires
                    sh 'python3 -m pip install --upgrade pip'
                    sh 'python3 -m pip install --ignore-installed -r requirements.txt'
                }
            }
        }
        stage('Prepare Data') {
            steps {
                script {
                    // Exécute la préparation des données avec les fichiers appropriés
                    sh 'python3 src/main.py --train data/churn-bigml-80.csv --test data/churn-bigml-20.csv --prepare'
                }
            }
        }
        stage('Train Model') {
            steps {
                script {
                    // Exécute l'entraînement du modèle avec les données d'entraînement et de test
                    sh 'python3 src/main.py --train data/churn-bigml-80.csv --test data/churn-bigml-20.csv --train'
                }
            }
        }
        stage('Evaluate Model') {
            steps {
                script {
                    // Exécute l'évaluation du modèle avec les données de test
                    sh 'python3 src/main.py --test data/churn-bigml-20.csv --evaluate'
                }
            }
        }
        stage('Deploy Model') {
            steps {
                script {
                    // Exécute le déploiement du modèle formé
                    sh 'python3 src/main.py --deploy'
                }
            }
        }
    }
    post {
        failure {
            echo 'Pipeline failed!'
        }
        success {
            echo 'Pipeline succeeded!'
        }
    }
}
