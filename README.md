# TDT4140-NIDALA
[![Build Status](https://travis-ci.org/mjansrud/TDT4140-NIDALA.svg?branch=master)](https://travis-ci.org/mjansrud/TDT4140-NIDALA)
[![codecov](https://codecov.io/gh/mjansrud/TDT4140-NIDALA/branch/master/graph/badge.svg)](https://codecov.io/gh/mjansrud/TDT4140-NIDALA)

NIDALA (NTNU Individually Dynamic Assigned Learning Assistant)

NIDALA is a project that aims to improve upon the many exercise programs on NTNU. <br />
Our idea of improvment is bade upon the concept of spaced repetition. <br />
Questions from previous excersices will show up on current excersices when NIDALA believes you need them repeated. <br />
If you stuggle with the same concepts over several assignments NIDALA will notify the teaching-staff, so they can help you <br />

NIDALA is developed using the Django Framework for Python 3.6

# Getting started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

**Optinal**<br />
Many of our developers have isolated their python-packeges for this project using virtualenv [read more](http://docs.python-guide.org/en/latest/dev/virtualenvs/)

Set your enviorment to be for Python 3.6+<br />
**/Optinal**

Make sure you have [**Python 3.6**](https://www.python.org/downloads/) and [**PIP**](http://stackoverflow.com/questions/6587507/how-to-install-pip-with-python-3) installed. Activate your virtural enviorment (if you have one) from here.

Clone the repository to a folder of your choice <br />
```
git clone https://github.com/mjansrud/TDT4140-NIDALA
```
If you do not have git installed do [click here](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

Navigate to the TDT4140-NIDALA folder
```
cd your/folder/of/choice/TDT4140-NIDALA
```
Install the required packages
```
pip install -r requirments.txt
```
The last pip command will install all the required python-packeges. There will most likely me some hangups here. Google is your friend.  
When this is done correctly, everything should be ready to go.
Run
```
python manage.py runserver
```
This command will run a local server that comes with Django. Be deafult the website will be running on your localhost (127.0.0.1:8000)<br />
##Authors
* Morten Jansrud <br />
* Kristian Haga <br />
* Martin Simensen <br />
* Håvard Opheim <br />

# Acknowledgments
* Pekka <br />

# Furhter reading
We will soon™ have a wiki. Should you have any further questions check our [wiki](https://github.com/mjansrud/TDT4140-NIDALA/wiki/)
