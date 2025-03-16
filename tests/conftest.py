import os

import pytest


@pytest.fixture(scope='session')
def docker_compose_file(pytestconfig) -> str:  # noqa: ANN001
    """Set the correct path for docker-compose.yml in tests/docker/"""
    return os.path.join(str(pytestconfig.rootdir), 'tests', 'docker', 'docker-compose.yml')
