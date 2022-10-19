pipeline {
  agent any
  stages {
    stage('Checkout Scm') {
      steps {
        git(credentialsId: 'RH', url: 'https://github.com/ict3x03-2022-team32/ict3x03-2022-team32.git')
      }
    }

    stage('No Converter-0') {
      steps {
        echo 'No converter for Builder: org.jenkinsci.plugins.DependencyCheck.DependencyCheckToolBuilder'
      }
    }

    stage('No Converter-1') {
      steps {
        echo 'No converter for Builder: com.cloudbees.jenkins.GitHubSetCommitStatusBuilder'
      }
    }

  }
  post {
    always {
      echo 'No converter for Publisher: org.jenkinsci.plugins.DependencyCheck.DependencyCheckPublisher'
      echo 'No converter for Publisher: com.cloudbees.jenkins.GitHubCommitNotifier'
    }

  }
}
