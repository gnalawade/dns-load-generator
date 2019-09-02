# ppdns_stress

PPDNS Stress is a DNS query load generator script written in Python3.

This forked version of PPDNS Stress leverages the Python [argparse](https://docs.python.org/3/library/argparse.html) module to accept user input and then generate UDP packets towards DNS servers.

## Demo
A demo of Flask Password can be found [here](https://www.icarustech.com/flask-password/).

## Screenshots

![Screenshot of script execution](docs/media/default_en.png "Script execution")

## Installation

**Method 1 - Run the Script**
1. Run the script! There are no dependencies.

**Method 2 - Create a Python Venv**
1. Browse to the project folder.
2. Create Python Virtual Environment [(venv)](https://docs.python.org/3/library/venv.html) and activate it.
3. Install the package requirements by running `pip install -r requirements.txt`.
4. Run the script!

```
cd ppdns_stress
python3 -m venv .
pip install -r requirements.txt
python ppdnstress.py
```

## Usage

This version of PPDNS Stress has been modified to include command line arguments. This is useful for generating queries quickly without needing to manually input settings every time.
