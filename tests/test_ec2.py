# -*- coding: utf-8 -*-
import click
from click.testing import CliRunner


def test_hello_world():
    @click.command()
    @click.argument('name')
    def hello(name):
        click.echo('Hello %s!' % name)

    runner = CliRunner()
    result = runner.invoke(hello, ['Peter'])
    assert result.exit_code == 0
    assert result.output == 'Hello Peter!\n'
