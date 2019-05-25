# Wal-O-Mat

[![Build Status](https://travis-ci.org/dieliste/walomat.svg?branch=master)](https://travis-ci.org/dieliste/walomat)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

## Setup

```
mkvirtualenv walomat
pip3 install -r requirements.txt
python3 manage.py migrate
python3 manage.py compilemessages
python3 manage.py collectstatic
python3 manage.py createsuperuser
```
