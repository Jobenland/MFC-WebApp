![size badge](https://img.shields.io/github/repo-size/Jobenland/MFC-WebApp.svg) ![license](https://img.shields.io/github/license/Jobenland/MFC-WebApp.svg) ![build](https://img.shields.io/badge/Build-Passing-green.svg) ![issues](https://img.shields.io/github/issues/Jobenland/MFC-WebApp.svg) ![Version](https://img.shields.io/badge/Version-1.0.0-blue.svg) ![python](https://img.shields.io/badge/Python-3.x-lightgrey.svg) ![toplang](https://img.shields.io/github/languages/top/Jobenland/MFC-WebApp.svg) ![quality](https://img.shields.io/badge/Code%20Quality-Testing...-red.svg)
# MFC Webapp

This program is meant to be ran on the same server that is running the MFC. In this case it has been developed for use in a RaspberryPi setup. Currently the app in in development mode so once completed should NOT be ran as a CLI command. 

This webapp contains user accounts to secure sending unauthorized querys to the server. the database has been auto created with a `Test` user account with the password `1234` for testing. When using on your own setup, recreating the database with your wanted credentails is the best method

Once one admin account is created and logged in, users can create accounts for other users to have authorized access to the MFC.


## Getting Started

create a virutal env

```bash
pyenv virtualenv venv
pyenv activate venv
pip install -r requirements.txt
```
or insteall the requirements
```
pip install -r requirements.txt
```
run `manage.py runserver` to start the server on `127.0.0.1:5000`
or run `manage.py runserver --host='<insert-ip-here>'` to start the server on the IP of the machine

to encrypt cookie/session edit line `9` of `config.py` by putting

and example would be
```python
class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = "b'\xdd\xfc\xcay}\xe5\x82\x9a\xff\xdc\xff\xe5[#\xb1\xbj'"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'
    SHOW_CAPTCHA = False
    RECAPTCHA_SITE_KEY = '<insert-your-site-key-here>'
    RECAPTCHA_SECRET_KEY = '<insert-your-secret-key-here>'
```

## Running the tests

if you are greeted with a message saying `* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)` the app is running and login screen should be visible at loopback

## Run Options

many options are availble for starting the server
* `manage.py runserver` starts the server on localhost loopback address
* `manage.py runserver --host=='<ip-here>'` starts the server on the IP listed
* `manage.py runserver --ssl-crt=='<cert-here>' --ssl-key=='<key-here>'` starts the server with ssl enabled. NOTE: Browsers will still identify this as unsecure becuase it will most likely be a self signed certificate

## Deployment

The best way to deploy is the combine `apache2` and this app together with something like `nginx` for security. For development, the best way is to create a shell script to launch the python program and then create a service out of the shell script to start the webapp on start.

example shell script
```shell
#!/bin/sh
# launcher.sh

cd /
cd home/pi/webapp/MFCW
python3 manage.py runserver --host=10.0.5.125
cd /
```

```shell
[unit]
Description=WebMFC
After=network.target

[Service]
ExecStart=/home/pi/launcher.sh
Restart=always

[Install]
WantedBy=default.target
```

## Built With


* [Pandas](https://pandas.pydata.org/) - Used to edit and read CSV's
* [NP](http://cs231n.github.io/python-numpy-tutorial/) - Help with scientific calculations
* [Flask](http://flask.palletsprojects.com/en/1.1.x/) - Help with creating python webapp
* [Bootstrap](https://getbootstrap.com/) - creating goodlooking UI
* [SQLite](https://www.sqlite.org/index.html) - Used for holding useraccounts
* [OpenSSL](https://www.openssl.org/) - Generating SSL keys and certificated

## Contributing

If any Enhancements, Features or Problems arrise, Please submit a request on github

## Versioning

No versioning control has been set up yet but I am working on having this work in the Future 

## Authors

* **Jonathan Obenland** - *Creating Webapp for use with MFC* - [Jonathan Obenland](https://github.com/jobenland)

## Credit

* **Daniel Abeles** - *Helped with code base* - [Den1al](https://www.twitter.com/Daniel_Abeles)

## License

This project is licensed under the MIT License
