# -*- coding: utf-8 -*-
import pytest
from jungle import cli


@pytest.mark.parametrize('emr_name', [
    ('*'),
    ('cluster-*'),
    ('cluster-02'),
    ('dummy-cluster'),
])
def test_emr_ls(runner, emr, emr_name):
    """jungle rds ls test"""
    result = runner.invoke(cli.cli, ['emr', 'ls', emr_name])
    assert result.exit_code == 0
