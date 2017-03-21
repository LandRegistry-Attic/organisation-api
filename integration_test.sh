# Get full path to the directory that this scripts is in
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# By changing to the directory that this script is in means you no longer need to be in
# the directory to run these tests
cd $DIR

pip install -r requirements.txt

py.test --junitxml=TEST-INT-flask-app-medium.xml --verbose --cov-report term-missing --cov application integration_tests

RESULT=$?

exit $RESULT
