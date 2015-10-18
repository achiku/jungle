# -*- coding: utf-8 -*-
import pytest

from jungle import cli


@pytest.mark.parametrize('elb_name', [
    (''),
    ('*'),
    ('loadbalancer-01'),
    ('loadbalancer*'),
    ('dummy-lb'),
])
def test_elb_ls(runner, elb, elb_name):
    """test for elb ls"""
    result = runner.invoke(cli.cli, ['elb', 'ls', elb_name])
    assert result.exit_code == 0


@pytest.mark.parametrize('elb_name', [
    (''),
    ('*'),
    ('loadbalancer-01'),
    ('loadbalancer*'),
    ('dummy-lb'),
])
def test_elb_ls_with_l(runner, elb, elb_name):
    """test for elb ls -l"""
    result = runner.invoke(cli.cli, ['elb', 'ls', '-l', elb_name])
    assert result.exit_code == 0
