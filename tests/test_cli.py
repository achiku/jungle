# -*- coding: utf-8 -*-
from jungle import cli


def test_cli(runner):
    """Basic test"""
    result = runner.invoke(cli.cli)
    assert result.exit_code == 0
    assert not result.exception
