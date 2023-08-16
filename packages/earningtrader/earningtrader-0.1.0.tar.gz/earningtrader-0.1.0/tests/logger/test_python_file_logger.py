import pathlib
import logging

import pytest

from earningtrader.controller._logger import PythonFileLogger


@pytest.fixture
def logger(tmp_path: pathlib.Path) -> PythonFileLogger:
    return PythonFileLogger(
        logger_name="test",
        filepath=str(tmp_path / "test.log"),
        message_format="%(asctime)s %(message)s",
    )


def test_logging_string(logger: PythonFileLogger):
    logger.log(message="test!", log_level=logging.INFO)

    with open(logger.filepath) as f:
        assert "test!" in " ".join(f.readlines())


def test_logging_exception(logger: PythonFileLogger):
    logger.log(message=ValueError("test!"), log_level=logging.ERROR)

    with open(logger.filepath) as f:
        assert "ValueError" in " ".join(f.readlines())
