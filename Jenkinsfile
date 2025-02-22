pipeline {
    agent any
    environment {
        GIT_TOKEN = credentials('token-oum')  // Utilise l'ID de l'identifiant GitHub
    }
    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/oumaiiima/MLOPS_project.git', credentialsId: 'token-oum'
            }
        }
        stage('Install Dependencies') {
            steps {
                script {
                    sh 'python3 -m pip install --upgrade pip'
                    sh 'python3 -m pip install --ignore-installed -r requirements.txt'
                }
            }
        }
        stage('Prepare Data') {
            steps {
                script {
                    sh 'python3 src/main.py --train data/train.csv --test data/test.csv --prepare'
                }
            }
        }
        stage('Train Model') {
            steps {
                script {
                    sh 'python3 src/main.py --train data/train.csv --test data/test.csv --train'
                }
            }
        }
        stage('Evaluate Model') {
            steps {
                script {
                    sh 'python3 src/main.py --test data/test.csv --evaluate'
                }
            }
        }
        stage('Deploy Model') {
            steps {
                script {
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
