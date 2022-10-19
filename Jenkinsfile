pipeline {
	agent any
	stages {
		stage('Checkout SCM') {
			steps {
				git branch:'main', url:'https://github.com/ict3x03-2022-team32/ict3x03-2022-team32'
			}
		}

		stage('OWASP DependencyCheck') {
			steps {
				dependencyCheck additionalArguments: '--format HTML --format XML', odcInstallation: 'Default'
			}
		}
	}	
	post {
		success {
			dependencyCheckPublisher pattern: 'dependency-check-report.xml'
		}
	}
}
