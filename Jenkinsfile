pipeline {
  agent any
  stages {
    stage('Checkout Scm') {
      steps {
        git(credentialsId: 'RH', branch:'development-testing', url: 'https://github.com/ict3x03-2022-team32/ict3x03-2022-team32.git')
      }
    }

    stage('OWASP DependencyCheck') {
			      steps {
				            dependencyCheck additionalArguments: '--format HTML --format XML --enableExperimental', odcInstallation: 'OWASP Dependency-Check'
			      }
		}
    stage('Test') {	
			      steps {
				            //git(credentialsId: 'RH', branch:'development-testing', url: 'https://github.com/ict3x03-2022-team32/ict3x03-2022-team32.git')
					    sh 'python3 --version'
					    sh 'JENKINS_NO_COOKIE=test nohup python3 -m pytest'
			      }
   	}
  }
	post {
		      success {
			      dependencyCheckPublisher pattern: 'dependency-check-report.xml'
			      setBuildStatus("Build succeeded", "SUCCESS");
		      }
		      failure {
			      setBuildStatus ("Build Failed", "FAILURE");
		      }
	}
}

void setBuildStatus(String message, String state) {
    step([
        $class: "GitHubCommitStatusSetter",
        reposSource: [$class: "ManuallyEnteredRepositorySource", url: "https://github.com/ict3x03-2022-team32/ict3x03-2022-team32"],
        contextSource: [$class: "ManuallyEnteredCommitContextSource", context: "SecurityCrusader"],
        errorHandlers: [[$class: "ChangingBuildStatusErrorHandler", result: "UNSTABLE"]],
        statusResultSource: [$class: "ConditionalStatusResultSource", results: [[$class: "AnyBuildResult", message: message, state: state]]]
    ]);
}
