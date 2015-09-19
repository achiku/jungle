# -*- coding: utf-8 -*-
import subprocess
import sys

import boto3
import botocore
import click


def format_output(instances, flag):
    """return formatted string for instance"""
    out = []
    line_format = '{}\t{}\t{}\t{}\t{}'
    name_len = _get_max_name_len(instances) + 3
    if flag:
        line_format = '{0:<' + str(name_len) + '}{1:<10}{2:<13}{3:<16}{4:<16}'

    for i in instances:
        tag_name = get_tag_value(i.tags, 'Name')
        out.append(line_format.format(
            tag_name, i.state['Name'], i.id, i.private_ip_address, str(i.public_ip_address)))
    return out


def _get_max_name_len(instances):
    # FIXME: ec2.instanceCollection doesn't have __len__
    for i in instances:
        return max([len(get_tag_value(i.tags, 'Name')) for i in instances])
    return 0


def get_tag_value(x, key):
    """Get a value from tag"""
    if x is None:
        return ''
    result = [y['Value'] for y in x if y['Key'] == key]
    if len(result) == 0:
        return ''
    return result[0]


@click.group()
def cli():
    """EC2 CLI group"""
    pass


@cli.command(help='List EC2 instances')
@click.argument('name', default='*')
@click.option('--list-formatted', '-l', is_flag=True)
def ls(name, list_formatted):
    """List EC2 instances"""
    ec2 = boto3.resource('ec2')
    if name == '*':
        instances = ec2.instances.filter()
    else:
        condition = {'Name': 'tag:Name', 'Values': [name]}
        instances = ec2.instances.filter(Filters=[condition])
    out = format_output(instances, list_formatted)
    click.echo('\n'.join(out))


@cli.command(help='Start EC2 instance')
@click.option('--instance-id', '-i', required=True, help='EC2 instance id')
def up(instance_id):
    """Start EC2 instance"""
    ec2 = boto3.resource('ec2')
    try:
        instance = ec2.Instance(instance_id)
        instance.start()
    except botocore.exceptions.ClientError as e:
        click.echo("Invalid instance ID {} ({})".format(instance_id, e), err=True)
        sys.exit(2)


@cli.command(help='Stop EC2 instance')
@click.option('--instance-id', '-i', required=True, help='EC2 instance id')
def down(instance_id):
    """Stop EC2 instance"""
    ec2 = boto3.resource('ec2')
    try:
        instance = ec2.Instance(instance_id)
        instance.stop()
    except botocore.exceptions.ClientError as e:
        click.echo("Invalid instance ID {} ({})".format(instance_id, e), err=True)
        sys.exit(2)


def create_ssh_command(instance_id, instance_name, username, key_file, port, gateway_instance_id):
    """Create SSH Login command string"""
    ec2 = boto3.resource('ec2')
    if instance_id is not None:
        try:
            instance = ec2.Instance(instance_id)
            hostname = instance.public_ip_address
        except botocore.exceptions.ClientError as e:
            click.echo("Invalid instance ID {} ({})".format(instance_id, e), err=True)
            sys.exit(2)
    elif instance_name is not None:
        try:
            condition = {'Name': 'tag:Name', 'Values': [instance_name]}
            instances = ec2.instances.filter(Filters=[condition])
            target_instances = []
            for idx, i in enumerate(instances):
                target_instances.append(i)
                tag_name = get_tag_value(i.tags, 'Name')
                click.echo('[{}]: {}\t{}\t{}\t{}'.format(
                    idx, i.id, i.private_ip_address, i.state['Name'], tag_name))
            selected_idx = click.prompt("Please enter a valid number", type=int, default=0)
            click.echo("{} is selected.".format(selected_idx))
            hostname = target_instances[selected_idx].public_ip_address
        except botocore.exceptions.ClientError as e:
            click.echo("Invalid instance ID {} ({})".format(instance_id, e), err=True)
            sys.exit(2)
    # TODO: need to refactor and make it testable
    if gateway_instance_id is not None:
        gateway_instance = ec2.Instance(gateway_instance_id)
        gateway_public_ip = gateway_instance.public_ip_address
        hostname = target_instances[selected_idx].private_ip_address
        cmd = 'ssh -tt ubuntu@{} -i {} -p {} ssh {}@{}'.format(
            gateway_public_ip, key_file, port, username, hostname)
    else:
        cmd = 'ssh {}@{} -i {} -p {}'.format(username, hostname, key_file, port)
    return cmd


@cli.command(help='SSH login to EC2 instance')
@click.option('--instance-id', '-i', default=None, help='EC2 instance id')
@click.option('--instance-name', '-n', default=None, help='EC2 instance Name Tag')
@click.option('--username', '-u', default='ubuntu', help='Login username')
@click.option('--key-file', '-k', required=True, help='SSH Key file path', type=click.Path())
@click.option('--port', '-p', help='SSH port', default=22)
@click.option('--gateway-instance-id', '-g', default=None, help='Gateway instance id')
@click.option('--dry-run', is_flag=True, default=False, help='Print SSH Login command and exist')
def ssh(instance_id, instance_name, username, key_file, port, gateway_instance_id, dry_run):
    """SSH to EC2 instance"""
    if instance_id is None and instance_name is None:
        click.echo(
            "One of --instance-id/-i or --instance-name/-n"
            " has to be specified.", err=True)
        sys.exit(2)
    elif instance_id is not None and instance_name is not None:
        click.echo(
            "Both --instance-id/-i and --instance-name/-n "
            "can't to be specified at the same time.", err=True)
        sys.exit(2)
    cmd = create_ssh_command(
        instance_id, instance_name, username, key_file, port, gateway_instance_id)
    if not dry_run:
        subprocess.call(cmd, shell=True)
    else:
        click.echo(cmd)
