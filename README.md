com_jrdbnntt_wedding
====================
Wedding website for Jared & Hannah!


## Project setup
### Dependencies
* `python3` - Python 3.8+
* `python3 -m venv` - Shipped with Python 3
* `nvm` - See https://github.com/nvm-sh/nvm

### Installation
Run `./server_install.sh` to configure the Python and Node.js environments.

### Running the server
#### Using the development webserver
```shell
$ source ./venv/bin/activate 
$ python3 manage.py runserver
```
Note: The process working directory *must* be the repository directory.


#### Using the ASGI application Daphne webserver
Run `./start_server.sh` to start the server. By default, it will run in `DEVELOPMENT`. To use a different runtime, set
the `RUNTIME_ENVIRONMENT` environment variable prior to running `./start_server.sh`.

Runtimes:
* `PRODUCTION`
* `TEST`
* `DEVELOPMENT`

Example:
```shell
$ ./server_start.sh
```
or
```shell
$ export RUNTIME_ENVIRONMENT=PRODUCTION; ./server_start.sh
```
Note: The process working directory *must* be the repository directory.
