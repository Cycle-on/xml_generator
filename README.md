Synthetic xml_data generator for 112 Department

# Start project

* * *

## Install python

_To start generator you need python3.12_\
https://www.python.org/downloads/

### Windows

1. Clone project(git clone git@github.com:Danchicic/xml_generator.git)
2. Go to directory and create venv (in directory in terminal: python -m venv venv)
3. Activate venv(windows terminal: venv\Scripts\activate)
4. Install requirements (pip install -r requirements.txt)

### OSX/Linux

1. Clone project(git clone git@github.com:Danchicic/xml_generator.git)
2. Go to directory and create venv (in directory: python3.12 -m venv venv)
3. Activate venv(bash: source venv/bin/activate)
4. Install requirements (pip install -r requirements.txt)

## Start conditionals

### 1. Copy the wsdl file to root of the project

❗️wsdl file must has name : wsdl_4_3.wsdl❗️

### *If you want to send files you need to fill the Environment

#### Start from terminal

1. Set global vars (guide for win: https://ab57.ru/cmdlist/set.html) like in the .env.example file

### Congratulations!

***

## Run: generator

### IDE

Launch main.py

### Terminal

in terminal with activated venv: python main.py

## Run: generator + sender

## Sender work only from terminal with --send flag

1. Fill global environment variables
2. [OPTIONAL] Choose type of sender in constants/sender.py(base=by_delay, delay=3)
3. [OPTIONAL] Choose prefixes for files in constants/sender.py
4. In terminal run command: python main.py --send

***

# Constants

### Local constants

You can change base values in constants directory in the root of project

1. generator - constants for generator, change it for locally start
2. sender - constants for sender module, change it, if you want to send files
3. union_constants - constants for all project(Date can be changed here),
   this file contains urls for google sheets

If constant has work_type postfix, you can change work_type_constant with one of: normal/poisson/uniform

### Google sheets constants

You can take constants from google sheet\
for this you need to change TAKE_CONSTANTS_FROM_FILE flag in generator to True

# Global vars

_You can add env variables to program_

#### SERVER VARS

SERVER_ADDRESS\
SERVER_PASSWORD\
SERVER_LOGIN

will be used if flag --send

# Terminal start params

You can launch the program with start values:

#### Params:

* --files-count <int> - files count to generate
* --xmls <int> - xml per file
* --date <str> - zero date for files in format <YYYY-MM-DD_HH-MM-SS>

#### Flags

* --send - work type for script
  if true files will be sent to address in global vars