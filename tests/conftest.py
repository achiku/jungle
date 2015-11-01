# -*- coding: utf-8 -*-
import boto3
import pytest
from click.testing import CliRunner
from moto import mock_ec2, mock_elb


@pytest.fixture
def runner():
    """Define test runner"""
    return CliRunner()


@pytest.yield_fixture(scope='function')
def elb():
    """ELB mock service"""
    mock = mock_elb()
    mock.start()

    client = boto3.client('elb')
    lbs = []
    for i in range(2):
        lb = client.create_load_balancer(
            LoadBalancerName='loadbalancer-01',
            Listeners=[
                {
                    'Protocol': 'http',
                    'LoadBalancerPort': 80,
                    'InstanceProtocol': 'http',
                    'InstancePort': 80,
                }
            ]
        )
        lbs.append(lb)
    yield {'lbs': lbs}
    mock.stop()


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
    gateway_server = ec2.create_instances(ImageId='ami-xxxxx', MinCount=1, MaxCount=1)
    servers = ec2.create_instances(ImageId='ami-xxxxx', MinCount=2, MaxCount=2)
    for i, s in enumerate(servers):
        ec2.create_tags(
            Resources=[s.id],
            Tags=[{'Key': 'Name', 'Value': 'server{:0>2d}'.format(i)}])

    yield dict(
        ec2=ec2,
        servers=servers,
        server=server[0],
        ssh_target_server=ssh_server[0],
        gateway_target_server=gateway_server[0],
    )

    mock.stop()
