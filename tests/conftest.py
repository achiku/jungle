# -*- coding: utf-8 -*-
import boto3
import pytest
from click.testing import CliRunner
from moto import mock_ec2


@pytest.fixture
def runner():
    """Define test runner"""
    return CliRunner()


@pytest.yield_fixture(scope='function')
def ec2():
    """EC2 mock service"""
    mock = mock_ec2()
    mock.start()

    ec2 = boto3.resource('ec2')
    ssh_server = ec2.create_instances(ImageId='ami-xxxxx', MinCount=1, MaxCount=1)
    for s in ssh_server:
        ec2.create_tags(
            Resources=[s.id],
            Tags=[{'Key': 'Name', 'Value': 'ssh_server'}])

    server = ec2.create_instances(ImageId='ami-xxxxx', MinCount=1, MaxCount=1)
    servers = ec2.create_instances(ImageId='ami-xxxxx', MinCount=2, MaxCount=2)
    for i, s in enumerate(servers):
        ec2.create_tags(
            Resources=[s.id],
            Tags=[{'Key': 'Name', 'Value': 'server{:0>2d}'.format(i)}])

    yield dict(
        ec2=ec2,
        servers=servers,
        server=server[0],
        ssh_server=ssh_server[0],
    )

    mock.stop()
