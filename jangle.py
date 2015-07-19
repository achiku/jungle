#!/usr/bin/env python
# -*- coding: utf-8 -*-
import click
import boto3


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
@click.option('--name', default='*bastion*', help='EC2 tag name')
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


@ec2.command(help='Start EC2 instances')
@click.option('--id', 'instance_id',
              required=True, help='EC2 instance id')
def up(instance_id):
    client = boto3.client('ec2')
    client.start_instances(InstanceIds=[instance_id])


@ec2.command(help='Stop EC2 instances')
@click.option('--id', 'instance_id',
              required=True, help='EC2 instance id')
def down(instance_id):
    client = boto3.client('ec2')
    client.stop_instances(InstanceIds=[instance_id])


if __name__ == '__main__':
    cli()
