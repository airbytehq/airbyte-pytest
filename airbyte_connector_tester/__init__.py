"""Test suites for Airbyte connectors."""

from airbyte_connector_tester.connector_tests import ConnectorTestSuiteBase
from airbyte_connector_tester.destination_tests import DestinationTestSuiteBase
from airbyte_connector_tester.source_tests import SourceTestSuiteBase

__all__ = [
    "ConnectorTestSuiteBase",
    "DestinationTestSuiteBase",
    "SourceTestSuiteBase",
]
