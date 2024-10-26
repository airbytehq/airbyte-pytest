import abc
from pathlib import Path

import pytest


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
