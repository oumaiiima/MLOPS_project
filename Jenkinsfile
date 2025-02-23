pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git branch: 'master', url: 'https://github.com/oumaiiima/MLOPS_project.git'
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
                // Exécuter les tests unitaires et d'intégration
                sh 'pytest tests/test_data_preparation.py -v'
                sh 'pytest tests/test_integration.py -v'
                sh 'pytest tests/test_model_evaluation.py -v'
                sh 'pytest tests/test_model_training.py -v'
                sh 'pytest tests/test_performance.py -v'
                sh 'pytest tests/test_predict.py -v'
                sh 'pytest tests/test_train_time.py -v'
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
