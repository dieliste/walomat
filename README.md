# Wal-O-Mat 🐋

[![Build Status](https://travis-ci.org/dieliste/walomat.svg?branch=master)](https://travis-ci.org/dieliste/walomat)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

The **Wal-O-Mat** – a simple and stupid voting advice application for student elections written in Django.

## Setup

It is recommended to create a virtual environment for this project, e.g. with [Virtualenv](https://virtualenv.pypa.io/en/stable/).

To install the dependencies run `pip3 install -r requirements.txt`.

Apply all database migrations and create the localized messages:

```
python3 manage.py migrate
python3 manage.py compilemessages
```

Add an admin user to your installation:

`python3 manage.py createsuperuser`

Start the Django server with `python3 manage.py runserver` and head to [http://localhost:8000/](http://localhost:8000/) with your favorite browser.

