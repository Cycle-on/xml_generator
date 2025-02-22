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
                if [ -d "/home/tester/xml_generator" ]; then
                  sudo chown -R ubuntu:ubuntu /home/tester/xml_generator  # Временно меняем владельца на ubuntu
                  rm -r /home/tester/xml_generator
                fi
                cp -r ~/jenkins_jobs/workspace/xml_generator /home/tester/
                sudo chown -R ubuntu:tester /home/tester/xml_generator  # Рекурсивно меняет владельца на tester:tester для всей папки
                sudo chmod 755 /home/tester/xml_generator  # Устанавливает права 755 для папки xml_generator
                sudo chmod 700 /home/tester/xml_generator/files  # Устанавливает права 700 для папки files (только владелец)
                sudo chmod 600 /home/tester/xml_generator/.env.example  # Устанавливает права 600 для файла .env.example (только владелец)
                sudo chmod 700 /home/tester/xml_generator/main.py  # Устанавливает права 700 для файла main.py (только владелец) 

                cd /home/tester/xml_generator/venv

                # Обновляем пути в виртуальном окружении
                OLD_PATH="/home/ubuntu/jenkins_jobs/workspace/xml_generator/venv"
                NEW_PATH="/home/tester/xml_generator/venv"
                find bin -type f -exec sed -i "s|$OLD_PATH|$NEW_PATH|g" {} +                
                echo "Done"
                '''
            }
        }
        
    }
}