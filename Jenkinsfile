pipeline {
    agent { node { label 'xml_generator' } }
    stages {
        stage ('Build'){
            steps{
                sh'''
                python3.12 -m venv venv
                . ./venv/bin/activate
                pip3.12 install -r requirements.txt                
                '''
            }
        }
        stage ('Cp to user tester'){
            steps{
                sh'''
                if [ -d "/home/tester/xml_generator" ]; then
                  sudo chown -R ubuntu:ubuntu /home/tester/xml_generator  # Временно меняем владельца на ubuntu
                  sudo rm -r /home/tester/xml_generator
                fi
                sudo cp -r ~/jenkins_jobs/workspace/xml_generator /home/tester/
                sudo chown -R ubuntu:tester /home/tester/xml_generator  # Рекурсивно меняет владельца на tester:tester для всей папки
                sudo chmod 755 /home/tester/xml_generator  # Устанавливает права 755 для папки xml_generator
                if [ -d "/home/tester/xml_generator/files" ]; then
                  sudo rm -r /home/tester/xml_generator/files
                fi
                sudo mkdir /home/tester/xml_generator/files
                sudo chmod 700 /home/tester/xml_generator/files  # Устанавливает права 700 для папки files (только владелец)
                sudo chmod 600 /home/tester/xml_generator/.env.example  # Устанавливает права 600 для файла .env.example (только владелец)
                sudo chmod 755 /home/tester/xml_generator/main.py # Устанавливает права 755 для файла main.py (только владелец, на запуск) 
                sudo cp -r /home/tester/wsdl_4_3.wsdl /home/tester/xml_generator/
                sudo chown -R tester:tester /home/tester/xml_generator
                

                cd /home/tester/xml_generator/venv

                # Обновляем пути в виртуальном окружении
                OLD_PATH="/home/ubuntu/jenkins_jobs/workspace/xml_generator/venv"
                NEW_PATH="/home/tester/xml_generator/venv"
                sudo find bin -type f -exec sed -i "s|$OLD_PATH|$NEW_PATH|g" {} +                
                
                sudo rm -r /home/tester/xml_generator/Jenkinsfile
                sudo rm -r /home/tester/xml_generator/todo.txt
                sudo rm -r /home/tester/xml_generator/ToDo.txt


                echo "Done"
                '''
            }
        }
    }
}
