pipeline {
    agent any
        stages{
            
            stage("Cloning from Github...."){
                steps{
                    script{
                        echo 'Cloning from Github...'
                        checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'Jenkinsdply', url: 'https://github.com/Saranya4537/EmployeeAttritionPrediction.git']])
                    }    
            }
        }
    }
}
