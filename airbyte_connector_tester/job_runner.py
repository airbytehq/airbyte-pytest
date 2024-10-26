import tempfile
import uuid
from pathlib import Path
from typing import Callable, Literal

import orjson
from airbyte_cdk.sources import Source
from airbyte_cdk.test import entrypoint_wrapper

from airbyte_connector_tester.test_models import AcceptanceTestInstance


def run_test_job(
    verb: Literal["read", "check", "discover"],
    test_instance: AcceptanceTestInstance,
    catalog: dict | None = None,
    *,
    source: Source | type[Source] | Callable[[], Source] | None = None,
) -> entrypoint_wrapper.EntrypointOutput:
    """Run a test job from provided CLI args and return the result."""
    source_obj: Source
    if isinstance(source, type):
        source_obj = source()
    elif isinstance(source, Source):
        source_obj = source
    elif isinstance(source, Callable):
        try:
            source_obj = source()
        except Exception as ex:
            if not test_instance.expect_exception:
                raise

            return entrypoint_wrapper.EntrypointOutput(
                messages=[],
                uncaught_exception=ex,
            )
    else:
        raise ValueError(f"Invalid source type: {type(source)}")

    args = [verb]
    if test_instance.config_path:
        args += ["--config", str(test_instance.config_path)]

    catalog_path: Path | None = None
    if verb not in ["discover", "check"]:
        if catalog:
            # Write the catalog to a temp json file and pass the path to the file as an argument.
            catalog_path = (
                Path(tempfile.gettempdir())
                / "airbyte-test"
                / f"temp_catalog_{uuid.uuid4().hex}.json"
            )
            catalog_path.parent.mkdir(parents=True, exist_ok=True)
            catalog_path.write_text(orjson.dumps(catalog).decode())
        elif test_instance.configured_catalog_path:
            catalog_path = Path(test_instance.configured_catalog_path)

        if catalog_path:
            args += ["--catalog", str(catalog_path)]

    # This is a bit of a hack because the source needs the catalog early.
    # Because it *also* can fail, we have ot redundantly wrap it in a try/except block.

    result: entrypoint_wrapper.EntrypointOutput = entrypoint_wrapper._run_command(  # noqa: SLF001  # Non-public API
        source=source_obj,
        args=args,
        expecting_exception=test_instance.expect_exception,
    )
    if result.errors and not test_instance.expect_exception:
        raise AssertionError(
            "\n\n".join(
                [str(err.trace.error).replace("\\n", "\n") for err in result.errors],
            )
        )

    if test_instance.expect_exception and not result.errors:
        raise AssertionError("Expected exception but got none.")  # noqa: TRY003

    return result
