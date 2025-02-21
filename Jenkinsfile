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
                rm -r /home/tester/xml_generator
                cp -r ~/jenkins_jobs/workspace/xml_generator /home/tester/
                sudo chown -R root:root /home/tester/xml_generator
                echo "Done"
                '''
            }
        }
        
    }
}