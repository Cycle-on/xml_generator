pipeline {
    agent { node { label 'xml_generator' } }
    stages {
        stage ('Build'){
            steps{
                sh'''
                python3.12 -m venv venv
                . ./venv/bin/activate
                pip install -r requirements.txt                
                '''
            }
        }
        stage ('Cp to user tester'){
            steps{
                sh'''
                cp ~/jenkins_jobs/workspace/xmml_generator /home/tester/
            }
        }
        
    }
}