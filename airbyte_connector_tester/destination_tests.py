from pathlib import Path

import pytest

from airbyte_connector_tester.connector_tests import ConnectorTestSuiteBase


class DestinationTestSuiteBase(ConnectorTestSuiteBase):
    """Base class for destination test suites."""
