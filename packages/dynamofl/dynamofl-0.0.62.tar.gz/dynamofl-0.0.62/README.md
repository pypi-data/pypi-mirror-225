# Run the samples

Try the samples to see the DynamoFL SDK in action.

## Generate API key from UI

## Setup the environment

Create and activate venv in the root of the repo. Use the windows equivalent commands if on Windows.

```bash
$ cd client-py
$ python -m venv venv
$ source venv/bin/active
```

Install the dependencies to the venv

```python
$ pip install -r requirements.txt
```

Install the dependencies of the samples/ folder

```python
$ cd client-py/samples && pip install -r requirements.txt
```

Create `.env` file.

```bash
$ cd client-py/samples
$ cp .env.template .env
```

Then set the `API_HOST` and `API_KEY` (generated from the UI) in `.env` file.

Run basic sample

```bash
$ python sample.py
```

# Development

## Install requirements

Create and activate venv in the root of the repo. Use the windows equivalent commands if on Windows.

```bash
$ cd client-py
$ python -m venv venv
$ source venv/bin/activate
```

Install the dependencies to the venv

```bash
$ pip install -r requirements.txt
```

Install pre commit hooks such as Black formatter

```bash
$ pre-commit install
```

## Tired of copy-pasting your latest changes into `site-packages` ?

Follow the steps below to run the `samples` against your latest code

1. Open `<venv>/bin/activate`
2. Paste the below code snippet to the end of file and set `CLIENT_PY_DIR`

```
CLIENT_PY_DIR=<absolute path to client-py repo>
SYSPATHS=$($VIRTUAL_ENV/bin/python -c "import sys; print(':'.join(x for x in sys.path if x))")
export PYTHONPATH=$SYSPATHS":"$CLIENT_PY_DIR
```

3. Run `pip uninstall dynamofl` to delete the `dynamofl` package from `site-packages`

<br>

> To test against a published `dynamofl` SDK, run `pip install dynamofl` before running the samples

# Build and publish the package

NOTE: Building the package would delete the `dist` directory and `dynamofl.egg-info` file at the root of `client-py`

1. Ensure the libraries listed in `client-py/requirements.txt` is installed in the venv
2. Activate the venv
3. Run `./build.sh`
