import os

from glean.utils.cli import getenv_bool


GLEAN_DEBUG = getenv_bool("GLEAN_DEBUG")
DEFAULT_CREDENTIALS_FILEPATH = "~/.glean/glean_access_key.json"
GLEAN_BASE_URI = os.environ.get("GLEAN_CLI_BASE_URI", default="https://glean.io")
FILE_SIZE_LIMIT_MB = 50
