# -*- coding: utf-8 -*-
import click


class JangleCLI(click.MultiCommand):

    """Jangle CLI main class"""

    def list_commands(self, ctx):
        """return available modules"""
        return ['ec2', 'elb']

    def get_command(self, ctx, name):
        """get command"""
        mod = __import__('jangle.' + name, None, None, ['cli'])
        return mod.cli


cli = JangleCLI(help='aws operation cli')


if __name__ == '__main__':
    cli()
