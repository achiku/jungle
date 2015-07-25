# -*- coding: utf-8 -*-
import click
import boto3
from botocore.exceptions import ClientError


def get_tag_value(x, key):
    result = [y['Value'] for y in x if y['Key'] == key]
    if len(result) == 0:
        return None
    return result[0]


@click.group()
def cli():
    pass


@cli.group()
def ec2():
    pass


@ec2.command(help='List EC2 instances')
@click.argument('name', default='*')
def ls(name):
    ec2 = boto3.resource('ec2')
    instances = ec2.instances.filter(
        Filters=[
            {'Name': 'tag:Name', 'Values': [name]},
        ]
    )
    for i in instances:
        instance_name = get_tag_value(i.tags, 'Name')
        click.echo('{}\t{}\t{}\t{}\t{}'.format(
            instance_name, i.state['Name'], i.id, i.private_ip_address, i.public_ip_address))


@ec2.command(help='Start EC2 instance')
@click.option('--instance-id', '-i', 'instance_id',
              required=True, help='EC2 instance id')
def up(instance_id):
    client = boto3.client('ec2')
    client.start_instances(InstanceIds=[instance_id])


@ec2.command(help='Stop EC2 instance')
@click.option('--instance-id', '-i', 'instance_id',
              required=True, help='EC2 instance id')
def down(instance_id):
    client = boto3.client('ec2')
    client.stop_instances(InstanceIds=[instance_id])


@cli.group()
def elb():
    pass


@elb.command(help='List ELB instances')
@click.argument('name', default='*')
def ls(name):
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
