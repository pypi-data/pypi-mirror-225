<p align="center">
  <img alt="logo" src="https://cdn.pixabay.com/photo/2014/04/02/10/21/lightning-303595_640.png" height="80">
  <h1 align="center">Cyberchief Bolt API Security</h1>
  <p align="center">Secure Your API.</p>
</p>

## Installation

Currently Cyberchief Bolt's Python Agent supports 2 servers:

- Django
- Flask

It can be installed from `pypi` by running :

```shell
pip install cyberchief-bolt
```

## Configuration

### Django

Once installed, Bolt's middleware can be added by modifying middlewares list (in the projects `settings.py`) like so:

```python
MIDDLEWARE = [
    ...,
    "bolt.django.BoltDjango",
] 
```

and configuring a `BOLT_CONFIG` attribute in the projects `settings.py` like this :

```python
BOLT_CONFIG = {
    "API_KEY": "<YOUR_BOLT_API_KEY>",
    "BOLT_HOST": "<YOUR_BOLT_COLLECTOR_URL>"
}
```

`BOLT_CONFIG` can take an optional key-value pair representing the max number of workers for communicating with Bolt.

### Flask

Once installed, Bolt middleware can be added simply like:

```python
from flask import Flask

...
from bolt.flask import BoltFlask

app = Flask(__name__)
BoltFlask(app, "<YOUR_BOLT_COLLECTOR_URL>", "<YOUR_BOLT_API_KEY>")
```

The Flask Middleware takes the flask app, Bolt collector url, and the Bolt API Key as parameters.

```python
BoltFlask(app, "<YOUR_BOLT_COLLECTOR_URL>", "<YOUR_BOLT_API_KEY>")
```