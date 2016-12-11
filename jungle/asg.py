# -*- coding: utf-8 -*-
import click
from jungle.session import create_session


def format_output(groups, flag):
    """return formatted string for instance"""
    out = []
    line_format = '{0}\t{1}\t{2}\t{3}\t{4}\t{5}'
    for g in groups['AutoScalingGroups']:
        out.append(line_format.format(
            g['AutoScalingGroupName'],
            g['LaunchConfigurationName'],
            'desired:'+str(g['DesiredCapacity']),
            'max:'+str(g['MaxSize']),
            'min:'+str(g['MinSize']),
            g['CreatedTime'].strftime('%Y/%m/%d %H:%M:%S'),
        ))
    return out


@click.group()
@click.option('--profile-name', '-P', default=None, help='AWS profile name')
@click.pass_context
def cli(ctx, profile_name):
    """AutoScaling CLI group"""
    ctx.obj = {}
    ctx.obj['AWS_PROFILE_NAME'] = profile_name


@cli.command(help='List AutoScaling groups')
@click.argument('name', default='*')
@click.option('--list-formatted', '-l', is_flag=True)
@click.pass_context
def ls(ctx, name, list_formatted):
    """List AutoScaling groups"""
    session = create_session(ctx.obj['AWS_PROFILE_NAME'])

    client = session.client('autoscaling')
    if name == "*":
        groups = client.describe_auto_scaling_groups()
    else:
        groups = client.describe_auto_scaling_groups(
            AutoScalingGroupNames=[
                name,
            ]
        )
    out = format_output(groups, list_formatted)
    click.echo('\n'.join(out))
