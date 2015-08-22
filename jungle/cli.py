# -*- coding: utf-8 -*-
import click


class JungleCLI(click.MultiCommand):

    """Jangle CLI main class"""

    def list_commands(self, ctx):
        """return available modules"""
        return ['ec2', 'elb']

    def get_command(self, ctx, name):
        """get command"""
        mod = __import__('jungle.' + name, None, None, ['cli'])
        return mod.cli


cli = JungleCLI(help='aws operation cli')


if __name__ == '__main__':
    cli()
