# -*- coding: utf-8 -*-
import boto3
import click
from botocore.exceptions import ClientError


def get_tag_value(x, key):
    """Get a value from tag"""
    result = [y['Value'] for y in x if y['Key'] == key]
    if len(result) == 0:
        return None
    return result[0]


@click.group()
def cli():
    """Main CLI group"""
    pass


@cli.group()
def ec2():
    """EC2 CLI group"""
    pass


@ec2.command(help='List EC2 instances')
@click.argument('name', default='*')
def ls(name):
    """List EC2 instances"""
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
    """Start EC2 instance"""
    client = boto3.client('ec2')
    client.start_instances(InstanceIds=[instance_id])


@ec2.command(help='Stop EC2 instance')
@click.option('--instance-id', '-i', 'instance_id',
              required=True, help='EC2 instance id')
def down(instance_id):
    """Stop EC2 instance"""
    client = boto3.client('ec2')
    client.stop_instances(InstanceIds=[instance_id])


@cli.group()
def elb():
    """ELB CLI group"""
    pass


@elb.command(help='List ELB instances')
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
