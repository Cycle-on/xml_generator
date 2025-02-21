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
                rm -r /home/tester/xml_generator/venv
                sudo chown -R tester:tester /home/tester/xml_generator
                sudo chown tester:tester /home/tester/xml_generator/main.py
                sudo chown tester:tester /home/tester/xml_generator/.env.example
                sudo chown -R tester:tester /home/tester/xml_generator/files # надо правильно настроить
                sudo chmod 700 /home/tester/xml_generator/files #надо исправить
                sudo chmod 755 /home/tester/xml_generator
                sudo chmod 600 /home/tester/xml_generator/.env.example  # Только редактирование
                sudo chmod 700 /home/tester/xml_generator/main.py  # Только выполнение
                
                echo "Done"
                '''
            }
        }
        
    }
}