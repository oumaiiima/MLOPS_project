pipeline {
    agent any
    
    environment {
        GITHUB_CREDENTIALS = credentials('github-token') // Remplacer par l'ID du credential
    }
    
    stages {
        stage('Clone Repository') {
            steps {
                script {
                    // Utiliser le token pour cloner le repo GitHub
                    sh """
                    git clone https://github.com/ton-utilisateur/ton-repository.git
                    """
                }
            }
        }
        
        stage('Build') {
            steps {
                // Étapes pour compiler ton projet ou exécuter des tests
                echo 'Build process'
            }
        }
        
        // Ajouter d'autres stages comme test, déploiement, etc.
    }
}
