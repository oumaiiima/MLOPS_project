pipeline {
    agent any
    environment {
        VENV_PATH = 'venv'
    }
    stages {
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
                    python3 -m pip install flake8 bandit
                '''
            }
        }
        stage('Quality Test') {
            steps {
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                    sh '''
                        . ${VENV_PATH}/bin/activate
                        flake8 src/ --count --select=E9,F63,F7,F82 --show-source --statistics
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
                        export PYTHONPATH=${WORKSPACE}
                        pytest --cov=src --cov-report=xml --junitxml=pytest_report.xml test/
                    '''
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'pytest_report.xml, coverage.xml', allowEmptyArchive: true
                }
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
                    python3 src/main.py --train-data data/train.csv --test data/test.csv --prepare
                '''
            }
        }
        stage('Train Model') {
            steps {
                sh '''
                    . ${VENV_PATH}/bin/activate
                    python3 src/main.py --train-data data/train.csv --test data/test.csv --train
                '''
            }
        }
        stage('Evaluate Model') {
            steps {
                sh '''
                    . ${VENV_PATH}/bin/activate
                    python3 src/main.py --train-data data/train.csv --test data/test.csv --evaluate
                '''
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
