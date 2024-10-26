import abc
from pathlib import Path

import pytest
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

    def test_use_plugin_test(self):
        assert True, "This is an example test"

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
        """Run acceptance tests."""
        result: entrypoint_wrapper.EntrypointOutput = run_test_job(
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
