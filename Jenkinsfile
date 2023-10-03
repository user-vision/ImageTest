def COLOR_MAP = ['SUCCESS': 'good', 'FAILURE': 'danger', 'UNSTABLE': 'danger', 'ABORTED': 'danger']

def notifyStarted() {
    office365ConnectorSend webhookUrl: 'https://outlook.office.com/webhook/540b2a75-1716-4171-b633-5d1f5d682730@f601d070-0902-4849-a88f-6a640b18d90a/JenkinsCI/8ad23b54b71b4f9285affd2b454114e4/9407d9b3-8106-42b6-a2e2-4a328bb51968',
        message: "Build Started)"
}

pipeline {
  agent any


  stages {
    stage('Get Issues') {
          steps {
            notifyStarted()
            withCredentials(bindings: [string(credentialsId: 'UVJenkins', variable: 'AUTH')]) {

          script {
            try {
              sh 'docker run --rm -v $(pwd):/app -e REPO=$REPO -e BRANCHES="$PROJECTS" -e AUTH=$AUTH -e PARENT="$PARENT" uservision/uv-python:latest'
            } catch (Exception e) {
              currentBuild.result = "FAILED"
              errorMsg = "FAILED TO CAPTURE ISSUES"
            }
          }     
              
     
            }
          }
        
    }

    stage('Build Report') {

          steps {
            withCredentials(bindings: [string(credentialsId: 'UVJenkins', variable: 'AUTH')]) {
          script {
            try {
              sh 'docker run --rm -v $(pwd):/app uservision/uv-a11yreport'
            } catch (Exception e) {
              currentBuild.result = "FAILED"
              errorMsg = "FAILED TO BUILD REPORT"
            }
          }     
              
              
            }

          }

    }
    // stage('Generate Powerpoint') {

    //       steps {
    //         withCredentials(bindings: [string(credentialsId: 'UVJenkins', variable: 'AUTH')]) {

    //       script {
    //         try {
    //             sh 'docker run --rm -v $(pwd):/app uservision/uv-ppt:pandoc'
    //         } catch (Exception e) {
    //           currentBuild.result = "FAILED"
    //           errorMsg = "FAILED TO GENERATE POWERPOINT"
    //         }
    //       }              
              
    //         }

    //       }

    // }
    stage('Generate PDF') {

          steps {
            withCredentials(bindings: [string(credentialsId: 'UVJenkins', variable: 'AUTH')]) {

          script {
            try {
                sh 'docker run --rm -v $(pwd):/app uservision/uv-pdf:pandoc'
            } catch (Exception e) {
              currentBuild.result = "FAILED"
              errorMsg = "FAILED TO GENERATE PDF"
            }
          }              
              
            }

          }

    }

    stage('Deploy') {
      steps {
        withCredentials(bindings: [string(credentialsId: 'zeit', variable: 'TOKEN')]) {

          script {
            try {
                sh 'docker run --rm -v $(pwd):/$TARGET uservision/uv-now:latest /bin/sh -c "now --prod --token $TOKEN -c deploy /$TARGET"'
            } catch (Exception e) {
              currentBuild.result = "FAILED"
              errorMsg = "FAILED TO DEPLOY"
            }
          }
          
          }
        }
    }


  }
  environment {
    REPO = 'user-vision/template-report'
    BRANCH = ' ADD BRANCH FROM REPO'
  // PROJECTS map to Github tags and will create separate chapters per tag in the report. To use multiple tags, separate with spaces
    PROJECTS = 'ADD PROJECT LABELS'
    PARENT = 'UVXXXX'
  // TARGET is the URL prefix used for the deployed report. It must be lowercase and contain only alphanumeric characters and dashes.
    TARGET = 'uvxxxx-client-expert-evaluation'
  }
  post {
    failure {
       office365ConnectorSend webhookUrl: 'https://outlook.office.com/webhook/540b2a75-1716-4171-b633-5d1f5d682730@f601d070-0902-4849-a88f-6a640b18d90a/JenkinsCI/8ad23b54b71b4f9285affd2b454114e4/9407d9b3-8106-42b6-a2e2-4a328bb51968',
            message: "# ${errorMsg}",
            status: 'Failure'      
        cleanWs()
    }
    success {
      office365ConnectorSend webhookUrl: 'https://outlook.office.com/webhook/540b2a75-1716-4171-b633-5d1f5d682730@f601d070-0902-4849-a88f-6a640b18d90a/JenkinsCI/8ad23b54b71b4f9285affd2b454114e4/9407d9b3-8106-42b6-a2e2-4a328bb51968',
            message: "# [${'https://' + env.TARGET + '.vercel.app'}](${'https://' + env.TARGET + '.vercel.app'})",
            status: 'Success'  
      cleanWs()
    }


  }
}

