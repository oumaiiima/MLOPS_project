pipeline {
    agent any

    environment {
        GITHUB_CREDENTIALS = credentials('github-token') // Remplacer 'github-token' par l'ID de ton credential
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'master',
                    url: "https://${GITHUB_CREDENTIALS}@github.com/oumaiiima/MLOPS_project.git"
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
                sh 'python3 src/main.py --train data/churn-bigml-80.csv --test data/churn-bigml-20.csv --prepare'
            }
        }
        stage('Train Model') {
            steps {
                sh 'python3 src/main.py --train data/churn-bigml-80.csv --test data/churn-bigml-20.csv --train'
            }
        }
        stage('Evaluate Model') {
            steps {
                sh 'python3 src/main.py --test data/churn-bigml-20.csv --evaluate'
            }
        }
        stage('Deploy Model') {
            steps {
                sh 'python3 src/main.py --deploy'
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
