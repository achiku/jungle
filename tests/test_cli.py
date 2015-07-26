# -*- coding: utf-8 -*-
import pytest
from click.testing import CliRunner

from jangle import cli


@pytest.fixture
def runner():
    """Define test runner"""
    return CliRunner()


def test_cli(runner):
    """Basic test"""
    result = runner.invoke(cli.cli)
    assert result.exit_code == 0
    assert not result.exception
