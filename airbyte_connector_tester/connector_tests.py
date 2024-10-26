import abc
from pathlib import Path
from typing import Any

import pytest
from airbyte_cdk import Connector
from airbyte_cdk.models import (
    AirbyteMessage,
    Type,
)
from airbyte_cdk.test import entrypoint_wrapper

from airbyte_connector_tester.job_runner import run_test_job
from airbyte_connector_tester.test_models import (
    AcceptanceTestInstance,
    get_acceptance_tests,
)


class ConnectorTestSuiteBase(abc.ABC):
    """Base class for connector test suites."""

    acceptance_test_file_path = Path("./acceptance-test-config.json")
    """The path to the acceptance test config file.

    By default, this is set to the `acceptance-test-config.json` file in
    the root of the connector source directory.
    """

    connector_class: type[Connector]
    """The connector class to test."""

    @abc.abstractmethod
    def new_connector(self, **kwargs: dict[str, Any]) -> Connector:
        """Create a new connector instance.

        By default, this returns a new instance of the connector class. Subclasses
        may override this method to generate a dynamic connector instance.
        """
        return self.connector_factory()

    @pytest.mark.parametrize(
        "test_input,expected",
        [
            ("3+5", 8),
            ("2+4", 6),
            ("6*9", 54),
        ],
    )
    def test_use_plugin_parametrized_test(
        self,
        test_input,
        expected,
    ):
        assert eval(test_input) == expected

    @pytest.mark.parametrize(
        "instance",
        get_acceptance_tests("connection"),
        ids=lambda instance: instance.instance_name,
    )
    def test_check(
        self,
        instance: AcceptanceTestInstance,
    ) -> None:
        """Run `connection` acceptance tests."""
        result: entrypoint_wrapper.EntrypointOutput = run_test_job(
            self.new_connector(),
            "check",
            test_instance=instance,
        )
        conn_status_messages: list[AirbyteMessage] = [
            msg for msg in result._messages if msg.type == Type.CONNECTION_STATUS
        ]  # noqa: SLF001  # Non-public API
        assert len(conn_status_messages) == 1, (
            "Expected exactly one CONNECTION_STATUS message. Got: \n"
            + "\n".join(result._messages)
        )
