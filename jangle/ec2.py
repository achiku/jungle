# -*- coding: utf-8 -*-
import getpass
import os
import socket
import sys
import traceback

import boto3
import click
import paramiko

from .utils import agent_auth, interactive_shell, manual_auth


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


@cli.command(help='SSH to EC2 instance')
@click.option('--instance-id', '-i', 'instance_id',
              required=True, help='EC2 instance id')
def ssh(instance_id):
    """SSH to EC2 instance"""
    client = boto3.client('ec2')
    instance = client.describe_instances(InstanceIds=[instance_id])
    click.echo(instance)

    # huge thanks to https://github.com/paramiko/paramiko/tree/master/demos
    username = 'ubuntu'
    hostname = instance['Reservations'][0]['Instances'][0]['PublicIpAddress']
    port = 22

    # now connect
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((hostname, port))
    except Exception as e:
        click.echo('*** Connect failed: ' + str(e))
        traceback.print_exc()
        sys.exit(1)

    try:
        t = paramiko.Transport(sock)
        try:
            t.start_client()
        except paramiko.SSHException:
            click.echo('*** SSH negotiation failed.')
            sys.exit(1)

        try:
            keys = paramiko.util.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
        except IOError:
            try:
                keys = paramiko.util.load_host_keys(os.path.expanduser('~/ssh/known_hosts'))
            except IOError:
                click.echo('*** Unable to open host keys file')
                keys = {}

        # check server's host key -- this is important.
        key = t.get_remote_server_key()
        if hostname not in keys:
            click.echo('*** WARNING: Unknown host key!')
        elif key.get_name() not in keys[hostname]:
            click.echo('*** WARNING: Unknown host key!')
        elif keys[hostname][key.get_name()] != key:
            click.echo('*** WARNING: Host key has changed!!!')
            sys.exit(1)
        else:
            click.echo('*** Host key OK.')

        # get username
        if username == '':
            default_username = getpass.getuser()
            username = input('Username [%s]: ' % default_username)
            if len(username) == 0:
                username = default_username

        agent_auth(t, username)
        if not t.is_authenticated():
            manual_auth(t, username, hostname)
        if not t.is_authenticated():
            click.echo('*** Authentication failed. :(')
            t.close()
            sys.exit(1)

        chan = t.open_session()
        chan.get_pty()
        chan.invoke_shell()
        click.echo('*** Here we go!\n')
        interactive_shell(chan)
        chan.close()
        t.close()

    except Exception as e:
        click.echo('*** Caught exception: ' + str(e.__class__) + ': ' + str(e))
        traceback.print_exc()
        try:
            t.close()
        except:
            pass
        sys.exit(1)
