def buildJobBlock(status_block) {
    def block = [
                    [
                        "type": "section",
                        "text": [
                            "type": "mrkdwn",
                            "text": "*Jenkins Build:* ${env.BUILD_TAG}/n*Github Branch:* ${env.BRANCH_NAME}"
                        ]
                    ],
                    [
                        "type": "divider"
                    ],
                    $status_block
                ]
    return $status_block
}

pipeline {
    agent {
        kubernetes {
            defaultContainer 'python'
            yaml '''
            apiVersion: v1
            kind: Pod
            spec:
              containers:
              - name: python
                image: nctiggy/python-build-image
                command:
                - sleep
                args:
                - 99d
            '''
        }
    }

    stages {
        stage('Print runtime versions') {
            steps {
                sh '''
                    python --version
                    ls -ltra
                    printenv
                    git --version
                    git remote show origin
                '''
            }
        }
        stage('Testing') {
            environment {
                COVERALLS_REPO_TOKEN = credentials('coverallsToken')
            }
            steps {
                sh '''
                    tox -e lint
                    tox -- --junitxml=junit-result.xml
                '''
                junit 'junit-result.xml'
            }
        }
        stage('Build pypi package') {
            when {
                buildingTag()
            }
            steps {
                sh 'tox -e build'
            }
        }
        stage('Publish pypi package') {
            when {
                buildingTag()
            }
            environment {
                TWINE = credentials('pypi_user_pass')
            }
            steps {
                sh '''
                    export TWINE_PASSWORD=$TWINE_PSW
                    export TWINE_USERNAME=$TWINE_USR
                    tox -e publish -- --repository pypi
                    tox -e clean
                '''
            }
        }
    }
}
