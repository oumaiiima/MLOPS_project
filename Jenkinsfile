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
        stage('Run Tests') {
            steps {
                sh 'pytest test/test_data_preparation.py --maxfail=1 --disable-warnings -q'
                sh 'pytest test/test_integration.py --maxfail=1 --disable-warnings -q'
                sh 'pytest test/test_model_evaluation.py --maxfail=1 --disable-warnings -q'
                sh 'pytest test/test_model_training.py --maxfail=1 --disable-warnings -q'
                sh 'pytest test/test_performance.py --maxfail=1 --disable-warnings -q'
                sh 'pytest test/test_predict.py --maxfail=1 --disable-warnings -q'
                sh 'pytest test/test_train_time.py --maxfail=1 --disable-warnings -q'
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
