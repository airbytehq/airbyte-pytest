"""Test suite for the connector tester."""

from airbyte_connector_tester import (
    ConnectorTestSuiteBase,
    DestinationTestSuiteBase,
    SourceTestSuiteBase,
)


class TestSourceTestSuite(SourceTestSuiteBase):
    """Test suite for source connectors."""


class TestDestinationTestSuite(DestinationTestSuiteBase):
    """Test suite for destination connectors."""


class TestConnectorTestSuite(ConnectorTestSuiteBase):
    """Test suite for connectors."""
