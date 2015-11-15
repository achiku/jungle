# -*- coding: utf-8 -*-
import boto3
import click


@click.group()
def cli():
    """EMR CLI group"""
    pass


@cli.command(help='List EMR clusters')
@click.argument('name', default='*')
def ls(name):
    """List EMR instances"""
    client = boto3.client('emr', region_name='us-east-1')
    results = client.list_clusters(
        ClusterStates=['RUNNING', 'STARTING', 'BOOTSTRAPPING', 'WAITING']
    )
    for cluster in results['Clusters']:
        click.echo(cluster['Id'])
