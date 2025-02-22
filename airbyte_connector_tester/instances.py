# Copyright (c) 2024 Airbyte, Inc., all rights reserved.

"""Run acceptance tests in PyTest.

These tests leverage the same `acceptance-test-config.yml` configuration files as the
acceptance tests in CAT, but they run in PyTest instead of CAT. This allows us to run
the acceptance tests in the same local environment as we are developing in, speeding
up iteration cycles.
"""

from __future__ import annotations

from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel

ACCEPTANCE_TEST_CONFIG_PATH = Path("acceptance-test-config.yml")


class AcceptanceTestInstance(BaseModel):
    """Acceptance test instance, as a Pydantic model.

    This class represents an acceptance test instance, which is a single test case
    that can be run against a connector. It is used to deserialize and validate the
    acceptance test configuration file.
    """

    class AcceptanceTestExpectRecords(BaseModel):
        path: Path
        exact_order: bool = False

    class AcceptanceTestFileTypes(BaseModel):
        skip_test: bool
        bypass_reason: str

    config_path: Path
    configured_catalog_path: Path | None = None
    timeout_seconds: int | None = None
    expect_records: AcceptanceTestExpectRecords | None = None
    file_types: AcceptanceTestFileTypes | None = None
    status: Literal["succeed", "failed"] | None = None

    @property
    def expect_exception(self) -> bool:
        return self.status and self.status == "failed"

    @property
    def instance_name(self) -> str:
        return self.config_path.stem


def get_acceptance_tests(
    category: str,
    accept_test_config_path: Path = ACCEPTANCE_TEST_CONFIG_PATH,
) -> list[AcceptanceTestInstance]:
    all_tests_config = yaml.safe_load(accept_test_config_path.read_text())
    if "acceptance_tests" not in all_tests_config:
        raise ValueError(
            f"Acceptance tests config not found in {accept_test_config_path}"
        )
    if category not in all_tests_config["acceptance_tests"]:
        return []
    if "tests" not in all_tests_config["acceptance_tests"][category]:
        raise ValueError(f"No tests found for category {category}")

    return [
        AcceptanceTestInstance.model_validate(test)
        for test in all_tests_config["acceptance_tests"][category]["tests"]
        if "iam_role" not in test["config_path"]
    ]
