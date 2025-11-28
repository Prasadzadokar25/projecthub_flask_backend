"""Compatibility shim for database connection.

This module existed previously at `app.database_connection.db_connection` and many
controllers import `get_db_connection` from here. The canonical centralized
implementation is `model.db.get_db_connection`. To avoid changing many imports
we delegate to `model.db` here.
"""
from model import db as model_db


def get_db_connection(*args, **kwargs):
    """Return a pymysql connection created by model.db.get_db_connection.

    Args are forwarded to the canonical implementation for future flexibility.
    """
    return model_db.get_db_connection(*args, **kwargs)


def get_db_cursor(connection=None):
    return model_db.get_db_cursor(connection)


def close_db_connection(connection):
    return model_db.close_db_connection(connection)
