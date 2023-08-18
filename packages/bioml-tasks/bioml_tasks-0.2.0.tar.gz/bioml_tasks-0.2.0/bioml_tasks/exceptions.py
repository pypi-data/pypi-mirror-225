class BioMlTasksException(Exception):
    pass


class BioMlTasksError(BioMlTasksException):
    """Raised when an error originates from the BioML Tasks API."""


class MlApiNotFoundError(BioMlTasksException):
    """Raised when trying to run an API that does not exist, or that the user doesn't have access to."""


class MlApiNotDeployedError(BioMlTasksException):
    """Raised when trying to run an API that is not deployed."""


class MlApiDeploymentError(BioMlTasksException):
    """Raised when trying to run an API that has been deployed but is not running. This is usually due to insufficient compute or incorrect setup code."""


class MlApiError(BioMlTasksException):
    """An error from the deployed ML API's code."""
