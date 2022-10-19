pipeline {
  agent any
  stages {
    stage('Checkout Scm') {
      steps {
        git(credentialsId: 'RH', branch:'main', url: 'https://github.com/ict3x03-2022-team32/ict3x03-2022-team32.git')
      }
    }

    stage('OWASP DependencyCheck') {
			      steps {
				            dependencyCheck additionalArguments: '--format HTML --format XML', odcInstallation: 'OWASP Dependency-Check'
			      }
		}
	}	
	post {
		      success {
			            dependencyCheckPublisher pattern: 'dependency-check-report.xml'
		      }
	}
}
