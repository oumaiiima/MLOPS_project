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
                sh 'python3 -m venv venv'
                sh '. venv/bin/activate && pip install --upgrade pip'
                sh '. venv/bin/activate && pip install --ignore-installed -r requirements.txt'
            }
        }
        stage('Run Tests') {
            steps {
                sh '. venv/bin/activate'
                sh 'export PYTHONPATH="${PYTHONPATH}:/root/.jenkins/workspace/job2/src"'
                sh 'echo "PYTHONPATH: ${PYTHONPATH}"'  // Affiche le PYTHONPATH pour vérification
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
                sh '. venv/bin/activate && python3 src/main.py --train-data data/train.csv --test data/test.csv --prepare'
            }
        }
        stage('Train Model') {
            steps {
                sh '. venv/bin/activate && python3 src/main.py --train-data data/train.csv --test data/test.csv --train'
            }
        }
        stage('Evaluate Model') {
            steps {
                sh '. venv/bin/activate && python3 src/main.py --train-data data/train.csv --test data/test.csv --evaluate'
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
