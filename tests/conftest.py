# -*- coding: utf-8 -*-
import pytest
from click.testing import CliRunner


@pytest.fixture
def runner():
    """Define test runner"""
    return CliRunner()
