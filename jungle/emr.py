# -*- coding: utf-8 -*-
import subprocess

import boto3
import click
from botocore.exceptions import ClientError


@click.group()
def cli():
    """EMR CLI group"""
    pass


@cli.command(help='List EMR clusters')
@click.argument('name', default='*')
def ls(name):
    """List EMR instances"""
    client = boto3.client('emr')
    results = client.list_clusters(
        ClusterStates=['RUNNING', 'STARTING', 'BOOTSTRAPPING', 'WAITING']
    )
    for cluster in results['Clusters']:
        click.echo("{0}\t{1}\t{2}".format(cluster['Id'], cluster['Name'], cluster['Status']['State']))


@cli.command(help='SSH to EMR master node')
@click.option('--cluster-id', '-i', required=True, help='EMR cluster id')
@click.option('--key-file', '-k', required=True, help='SSH Key file path', type=click.Path())
def ssh(cluster_id, key_file):
    """SSH login to EMR master node"""
    client = boto3.client('emr')
    result = client.describe_cluster(ClusterId=cluster_id)
    target_dns = result['Cluster']['MasterPublicDnsName']
    ssh_options = '-o StrictHostKeyChecking=no -o ServerAliveInterval=10'
    cmd = 'ssh {ssh_options}  -i {key_file} hadoop@{target_dns}'.format(
        ssh_options=ssh_options, key_file=key_file, target_dns=target_dns)
    subprocess.call(cmd, shell=True)


@cli.command(help='Terminate a EMR cluster')
@click.option('--cluster-id', '-i', required=True, help='EMR cluster id')
def rm(cluster_id):
    """Terminate a EMR cluster"""
    client = boto3.client('emr')
    try:
        result = client.describe_cluster(ClusterId=cluster_id)
        target_dns = result['Cluster']['MasterPublicDnsName']
        flag = click.prompt(
            "Are you sure you want to terminate {0}: {1}? [y/Y]".format(
                cluster_id, target_dns), type=str, default='n')
        if flag.lower() == 'y':
            result = client.terminate_job_flows(JobFlowIds=[cluster_id])
    except ClientError as e:
        click.echo(e, err=True)
