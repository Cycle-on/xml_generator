Synthetic xml_data generator for 112 Department

# Start project

* * *

## Install python

_To start parser you need python3.12_\
https://www.python.org/downloads/

## Windows

1. Clone project(git clone git@github.com:Danchicic/xml_generator.git)
2. Go to directory and create venv (in directory: python -m venv venv)
3. Activate venv(windows terminal: venv\Scripts\activate)
4. Install requirements (pip install -r requirements.txt)

## OSX/Linux

1. Clone project(git clone git@github.com:Danchicic/xml_generator.git)
2. Go to directory and create venv (in directory: python3.12 -m venv venv)
3. Activate venv(bash: source venv/bin/activate)
4. Install requirements (pip install -r requirements.txt)

### Congratulations!

***

# Constants

You can change base values in constants.py in the root of project

If constant has work_type, you can change work_type_constant with one of: normal/poisson/uniform

# Global vars

_You can add env variables to program_

#### SERVER VARS

will be used if flag --send
SERVER_ADDRESS
SERVER_PASSWORD
SERVER_LOGIN

# Start params

You can launch the program with start values:

#### Params:

* --files-count <int> - files count to generate
* --xmls <int> - xml per file
* --date <str> - zero date for files in format <YYYY-MM-DD_HH-MM-SS>

#### Flags

* --send - work type for script
  if true files will be sent to address in global vars