# -*- coding: utf-8 -*-
import click
from botocore.exceptions import ClientError
from jungle.session import create_session


@click.group()
@click.option('--profile-name', '-P', default=None, help='AWS profile name')
@click.pass_context
def cli(ctx, profile_name):
    """ELB CLI group"""
    ctx.obj = {'AWS_PROFILE_NAME': profile_name}


@cli.command(help='List ELB instances')
@click.argument('name', default='*')
@click.option('--list-instances', '-l', 'list_instances', is_flag=True, help='List attached EC2 instances')
@click.pass_context
def ls(ctx, name, list_instances):
    """List ELB instances"""
    session = create_session(ctx.obj['AWS_PROFILE_NAME'])

    client = session.client('elb')
    inst = {'LoadBalancerDescriptions': []}
    if name == '*':
        inst = client.describe_load_balancers()
    else:
        try:
            inst = client.describe_load_balancers(LoadBalancerNames=[name])
        except ClientError as e:
            click.echo(e, err=True)

    for i in inst['LoadBalancerDescriptions']:
        click.echo(i['LoadBalancerName'])
        if list_instances:
            for ec2 in i['Instances']:
                health = client.describe_instance_health(
                    LoadBalancerName=name,
                    Instances=[ec2]
                )
                click.echo('{0}\t{1}'.format(ec2['InstanceId'], health['InstanceStates'][0]['State']))
