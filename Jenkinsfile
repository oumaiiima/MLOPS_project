pipeline {
    agent any
    environment {
        VENV_PATH = 'venv'
        MLFLOW_TRACKING_URI = 'http://localhost:5001'  // URI de suivi MLflow
    }
    stages {
        stage('Clean Workspace') {
            steps {
                sh '''
                    # Nettoyer les artefacts précédents
                    rm -rf ${VENV_PATH}
                    rm -f security_report.json pytest_report.xml coverage.xml mlflow_metrics.json
                '''
            }
        }
        stage('Checkout') {
            steps {
                git branch: 'master', url: 'https://github.com/oumaiiima/MLOPS_project.git'
            }
        }
        stage('Setup Python Environment') {
            steps {
                sh '''
                    python3 -m venv ${VENV_PATH}
                    . ${VENV_PATH}/bin/activate
                    python3 -m pip install --upgrade pip
                    python3 -m pip install --ignore-installed -r requirements.txt
                    python3 -m pip install flake8 bandit pytest pytest-cov
                '''
            }
        }
        stage('Prepare Data') {
            steps {
                sh '''
                    . ${VENV_PATH}/bin/activate
                    if [ ! -f data/train.csv ] || [ ! -f data/test.csv ]; then
                        echo "Missing dataset files!"
                        exit 1
                    fi
                    python3 src/main.py --train data/train.csv --test data/test.csv --prepare
                '''
            }
        }
        stage('Train Model') {
            steps {
                sh '''
                    . ${VENV_PATH}/bin/activate
                    python3 src/main.py --train data/train.csv --test data/test.csv --mlflow --register
                '''
            }
        }
        stage('Evaluate Model') {
            steps {
                sh '''
                    . ${VENV_PATH}/bin/activate
                    python3 src/main.py --train data/train.csv --test data/test.csv --evaluate
                '''
            }
        }
        stage('Quality Test') {
            steps {
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                    sh '''
                        . ${VENV_PATH}/bin/activate
                        flake8 src/ --count --select=E9,F63,F7,F82 --show-source --statistics --exclude=venv
                    '''
                }
            }
        }
        stage('Security Test') {
            steps {
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                    sh '''
                        . ${VENV_PATH}/bin/activate
                        bandit -r src/ -f json -o security_report.json
                    '''
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'security_report.json', allowEmptyArchive: true
                }
            }
        }
        stage('Unit Tests') {
            steps {
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                    sh '''
                        . ${VENV_PATH}/bin/activate
                        export PYTHONPATH=${WORKSPACE}  # Ajouter le répertoire de travail au PYTHONPATH
                        pytest --cov=src --cov-report=xml --junitxml=pytest_report.xml test/  # Exécuter les tests unitaires
                    '''
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'pytest_report.xml, coverage.xml', allowEmptyArchive: true
                }
            }
        }
        stage('Extract MLflow Metrics') {
            steps {
                sh '''
                    . ${VENV_PATH}/bin/activate
                    python3 src/extract_metrics.py || echo "Aucune run trouvée, génération d'un fichier vide."
                    touch mlflow_metrics.json  # Crée un fichier vide si aucun n'existe
                '''
            }
            post {
                always {
                    archiveArtifacts artifacts: 'mlflow_metrics.json', allowEmptyArchive: true
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
