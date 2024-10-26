from pathlib import Path

import pytest

from airbyte_connector_tester.connector_tests import ConnectorTestSuiteBase


class SourceTestSuiteBase(ConnectorTestSuiteBase):
    """Base class for source test suites."""

    acceptance_test_file_path = Path("./acceptance-test-config.json")
