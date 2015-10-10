# -*- coding: utf-8 -*-
from jungle import cli


def test_elb_ls(runner, elb):
    """test for elb ls"""
    result = runner.invoke(cli.cli, ['elb', 'ls'])
    assert result.exit_code == 0


def test_elb_ls_with_l(runner, elb):
    """test for elb ls -l"""
    result = runner.invoke(cli.cli, ['elb', 'ls', '-l'])
    assert result.exit_code == 0
