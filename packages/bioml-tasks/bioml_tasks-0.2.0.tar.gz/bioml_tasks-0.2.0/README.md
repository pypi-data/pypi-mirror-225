# BioML Tasks Python client

This is a Python client for [BioML Tasks](https://biomltasks.com/v4). It lets you run ML APIs from your Python code or Jupyter notebook.

## Install

```sh
pip install bioml_tasks
```

## Authenticate

Before running any Python scripts that use the API, you need to set your BioML Tasks API token in your environment.

Grab your token from [biomltasks.com/settings](https://biomltasks.com/settings) and set it as an environment variable:

```
export BIOML_TASKS_API_TOKEN=<your token>
```

We recommend not adding the token directly to your source code, because you don't want to put your credentials in source control. If anyone used your API key, their usage would be charged to your account.

## Run a model

Create a new Python file and add the following code:

```python
>>> import bioml_tasks
>>> bioml_tasks.run(
        "<user_name>/<api_name>",
        input={"prompt": "a 19th century portrait of a wombat gentleman", "another_arg": "its value"}
    )

```

## Errors and Exceptions
- `bioml_tasks.exceptions.MlApiNotFoundError` - Raised when trying to run an API that does not exist, or that the user doesn't have access to.
- `bioml_tasks.exceptions.MlApiNotDeployedError` - Raised when trying to run an API that exists, but is not deployed.
- `bioml_tasks.exceptions.MlApiDeploymentError` - Raised when trying to run an API that has been deployed but is not running. This is usually due to insufficient compute or incorrect setup code.
- `bioml_tasks.exceptions.MlApiError` - An error from the deployed ML API.
- `bioml_tasks.exceptions.BioMlTasksError` - A generic error for all other errors.
- `bioml_tasks.exceptions.BioMlTasksException` - The base class that all the above errors inherit from.

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md)
