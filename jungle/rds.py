# -*- coding: utf-8 -*-
import click
from jungle.session import create_session


def format_output(instances, flag):
    """return formatted string per instance"""
    out = []
    line_format = '{0}\t{1}\t{2}\t{3}'
    name_len = _get_max_name_len(instances) + 3
    if flag:
        line_format = '{0:<' + str(name_len+5) + '}{1:<16}{2:<65}{3:<16}'

    for i in instances:
        endpoint = "{0}:{1}".format(i['Endpoint']['Address'], i['Endpoint']['Port'])
        out.append(
            line_format.format(i['DBInstanceIdentifier'], i['DBInstanceStatus'], endpoint, i['Engine']))
    return out


def _get_max_name_len(instances):
    """get max length of Tag:Name"""
    for i in instances:
        return max([len(i['DBInstanceIdentifier']) for i in instances])
    return 0


@click.group()
@click.option('--profile-name', '-P', default=None, help='AWS profile name')
@click.pass_context
def cli(ctx, profile_name):
    """RDS CLI group"""
    ctx.obj = {'AWS_PROFILE_NAME': profile_name}


@cli.command(help='List RDS instances')
@click.option('--list-formatted', '-l', is_flag=True)
@click.pass_context
def ls(ctx, list_formatted):
    """List RDS instances"""
    session = create_session(ctx.obj['AWS_PROFILE_NAME'])

    rds = session.client('rds')
    instances = rds.describe_db_instances()
    out = format_output(instances['DBInstances'], list_formatted)
    click.echo('\n'.join(out))
