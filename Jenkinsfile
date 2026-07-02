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

            stage("Making a virtual environment...."){
                steps{
                    script{
                        echo 'Making a virtual environment...'
                        sh '''
                        python -m venv ${VENV_DIR}
                        . ${VENV_DIR}/bin/activate
                        pip install --upgrade pip
                        pip install -e .
                        pip install  dvc
                        '''
                    }
                }
            }
        }
    }
