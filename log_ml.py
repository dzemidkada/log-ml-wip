#!/usr/bin/env python
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
LOGML_ROOT = os.path.join(PROJECT_ROOT, 'src')
sys.path.append(LOGML_ROOT)

import click

from logml.eda_tools import main as eda
from logml.commons.click_utils import add_click_commands


@add_click_commands(
    eda.main
)
@click.group('logml')
def logml_main():
    pass


def main(env_variables=None):
    """
    Run logml_main within a custom environment.
    :param env_variables: dict
        The mapping for custom environment variables: name -> value.
        These variables will be set before the logml_main execution
        and cleared right after it.
    """
    if env_variables is None:
        env_variables = {}

    _environ = os.environ.copy()
    try:
        os.environ.update(env_variables)
        logml_main()
    finally:
        os.environ.clear()
        os.environ.update(_environ)


if __name__ == '__main__':
    main(env_variables={
        'PROJECT_ROOT': PROJECT_ROOT,
        'PYTHONPATH': os.pathsep.join(sys.path),
    })
