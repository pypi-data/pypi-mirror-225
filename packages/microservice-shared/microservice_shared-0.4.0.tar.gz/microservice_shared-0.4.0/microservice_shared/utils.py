"""
Utility functions for microservice_shared package.
"""
import os


def create_directories(log_directories) -> None:
    """Creates the log directories.

    Returns:
        None.
    """
    for directory in log_directories:
        os.makedirs(directory, exist_ok=True)
