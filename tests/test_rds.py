# -*- coding: utf-8 -*-
from jungle import cli


def test_rds_ls(runner, rds):
    """jungle rds ls test"""
    result = runner.invoke(cli.cli, ['rds', 'ls'])
    assert result.exit_code == 0


def test_rds_ls_with_l(runner, rds):
    result = runner.invoke(cli.cli, ['rds', 'ls', '-l'])
    assert result.exit_code == 0
