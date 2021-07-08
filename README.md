## Pytest UI framework

```sh

├── common                      //< common classes and methods
│   ├── ui                      //< ui package 
│   |   ├── config              //< general configuration classes
│   |   ├── pageobjects         //< page objects
│   ├── utils   
├── tests                       //< tests package
│   ├── ui                      //< ui tests and related classes
│   Pipfile                     //< required libraries
│   Pytest.ini                  //< Pytest configuration file
│   README.md                   //< Starting guideline
```

## Getting Started

This is the quick and easy getting started assuming you already have git and pip installed.

```sh

# navigate home directory
cd ~/thachhoang-unitlists-pytest

# Install the required items
1. Remove your current version of virtualenv (optional)
pip uninstall virtualenv

2. Install pipenv
pip install --user pipenv

3. Testing the installation
pipenv --version

4. Install dependencies
pipenv install Pipfile 
If you have multiple python version use below command
pipenv install --python=/usr/bin/<python_directory> Pipfile

5. Switch to pipenv virtual environment
pipenv shell

If you want to upgrade changes in Pipfile? Just do $ pipenv update. 
For more details please refer https://docs.pipenv.org/en/latest/basics/

6. Run tests 
# To run all scenarios:
pytest -m full_regression


## Run test with Parallel mode
Below are 2 options to run parallel:
- To send tests to multiple CPUs, type:
```pytest -n <number of CPUs> -m full_regression```

- Running tests in a Python subprocess
```pytest -d --tx <number of sub processes>*popen//python=python -m full_regression```

## Report generating
This report required allure cli, please refer this link to install https://docs.qameta.io/allure/#_installing_a_commandline

Follow below step to trigger test and generate report
```sh
# run test with this command
pytest --alluredir=allure_results

# generate report from the results.
allure serve allure_results
```

## IDE

### PyCharm

https://www.jetbrains.com/pycharm/

Debug configuration: https://www.jetbrains.com/help/pycharm/run-debug-configuration-py-test.html
