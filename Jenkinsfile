pipeline {
    agent { node { label 'xml_generator' } }
    stages {
        stage ('Build'){
            steps{
                sh'''
                python3.12 -m venv venv
                source venv/bin/active
                pip install -r requirements.txt                
                '''
            }
        }
    }
}