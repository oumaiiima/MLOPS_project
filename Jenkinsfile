pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git branch: 'master', url: 'https://github.com/oumaiiima/MLOPS_project.git'
            }
        }
        stage('Check Files') {
            steps {
                sh 'ls -R'  // Liste tous les fichiers et dossiers
            }
        }
        stage('Install Dependencies') {
            steps {
                sh 'python3 -m pip install --upgrade pip'
                sh 'python3 -m pip install --ignore-installed -r requirements.txt'
            }
        }
        stage('Run Tests') {
            steps {
                // Exécuter les tests depuis le dossier "test"
                sh 'pytest test/test_data_preparation.py -v'
                sh 'pytest test/test_integration.py -v'
                sh 'pytest test/test_model_evaluation.py -v'
                sh 'pytest test/test_model_training.py -v'
                sh 'pytest test/test_performance.py -v'
                sh 'pytest test/test_predict.py -v'
                sh 'pytest test/test_train_time.py -v'
            }
        }
        stage('Prepare Data') {
            steps {
                sh 'python3 src/main.py --train-data data/train.csv --test data/test.csv --prepare'
            }
        }
        stage('Train Model') {
            steps {
                sh 'python3 src/main.py --train-data data/train.csv --test data/test.csv --train'
            }
        }
        stage('Evaluate Model') {
            steps {
                sh 'python3 src/main.py --train-data data/train.csv --test data/test.csv --evaluate'
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
