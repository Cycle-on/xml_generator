pipeline {
    { node { label 'xml_generator' } }
    stages {
        stage ('Test'){
            steps{
                scripts{
                    sh '''
                    echo "Test agent ${env.NODE_NAME}"
                    '''
                }
            }
        }
    }
}