pipeline {
    agent { node { label 'xml_generator' } }
    stages {
        stage ('Test'){
            steps{
                    sh '''
                    echo "Test agent"
                    '''
            }
        }
    }
}