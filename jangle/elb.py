# -*- coding: utf-8 -*-
import boto3
import click
from botocore.exceptions import ClientError


@click.group()
def cli():
    """ELB CLI group"""
    pass


@cli.command(help='List ELB instances')
@click.argument('name', default='*')
@click.option('--list-instances', '-l', 'list_instances', is_flag=True, help='List attached EC2 instances')
def ls(name, list_instances):
    """List ELB instances"""
    client = boto3.client('elb')
    inst = {'LoadBalancerDescriptions': []}
    if name == '*':
        inst = client.describe_load_balancers()
    else:
        try:
            inst = client.describe_load_balancers(LoadBalancerNames=[name])
        except ClientError:
            pass

    for i in inst['LoadBalancerDescriptions']:
        click.echo(i['LoadBalancerName'])
        if list_instances:
            for ec2 in i['Instances']:
                health = client.describe_instance_health(
                    LoadBalancerName=name,
                    Instances=[ec2]
                )
                click.echo('{}\t{}'.format(ec2['InstanceId'], health['InstanceStates'][0]['State']))
