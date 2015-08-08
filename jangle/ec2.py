# -*- coding: utf-8 -*-
import boto3
import click


def get_tag_value(x, key):
    """Get a value from tag"""
    result = [y['Value'] for y in x if y['Key'] == key]
    if len(result) == 0:
        return None
    return result[0]


@click.group()
def cli():
    """EC2 CLI group"""
    pass


@cli.command(help='List EC2 instances')
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


@cli.command(help='Start EC2 instance')
@click.option('--instance-id', '-i', 'instance_id',
              required=True, help='EC2 instance id')
def up(instance_id):
    """Start EC2 instance"""
    client = boto3.client('ec2')
    client.start_instances(InstanceIds=[instance_id])


@cli.command(help='Stop EC2 instance')
@click.option('--instance-id', '-i', 'instance_id',
              required=True, help='EC2 instance id')
def down(instance_id):
    """Stop EC2 instance"""
    client = boto3.client('ec2')
    client.stop_instances(InstanceIds=[instance_id])
