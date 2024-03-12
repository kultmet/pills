import os

from dotenv import load_dotenv
from sentry_sdk import capture_exception, push_scope

load_dotenv()

DB_NAME = os.getenv("POSTGRES_NAME", default="postgres")
DB_USERNAME = os.getenv("POSTGRES_USER", default="postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", default="postgres")
DB_HOST = os.getenv("POSTGRES_HOST", default="localhost")
DB_PORT = os.getenv("POSTGRES_PORT", default=5432)

REDIS_HOST = os.getenv("REDIS_HOST", default="localhost")
REDIS_PORT = os.getenv("REDIS_PORT", default=6379)
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", default="")
REDIS_DB = os.getenv("REDIS_DB", default=1)

DEBUG = os.getenv("DEBUG", default="True") == "True"


def push_sentry_message(exception):
    with push_scope() as scope:
        scope.fingerprint = [str(exception)]
        capture_exception(exception)
