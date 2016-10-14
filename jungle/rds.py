# -*- coding: utf-8 -*-
import subprocess
import sys

import boto3
import botocore
import click

def format_output(instances, flag):
    """return formatted string for instance"""
    out = []
    line_format = '{0}\t{1}'
    name_len = _get_max_name_len(instances) + 3
    if flag:
        line_format = '{0:<' + str(name_len) + '}{1:<16}{2:<21}{3:<16}{4:<16}'

    for i in instances:
        tag_name = i['DBInstanceIdentifier']
        out.append(line_format.format(i['DBInstanceIdentifier'], i['Endpoint']['Address']))
    return out


def _get_max_name_len(instances):
    """get max length of Tag:Name"""


    for i in instances:
        return max([len(i['DBInstanceIdentifier']) for i in instances])
    return 0


def get_tag_value(x, key):
    """Get a value from tag"""
    if x is None:
        return ''
    result = [y['Value'] for y in x if y['Key'] == key]
    if result:
        return result[0]
    return ''

@click.group()
def cli():
    """RDS CLI group"""
    pass

@cli.command(help='List RDS instances')
@click.argument('name', default='*')
@click.option('--list-formatted', '-l', is_flag=True)
def ls(name, list_formatted):
    """List EC2 instances"""
    rds = boto3.client('rds')
    if name == '*':
        instances = rds.describe_db_instances()
    else:
        condition = {'Name': 'tag:Name', 'Values': [name]}
        instances = rds.describe_db_instances(Filters=[condition])
    out = format_output(instances['DBInstances'], list_formatted)
    click.echo('\n'.join(out))
