# -*- coding: utf-8 -*-
import os

import boto3
import pytest
from click.testing import CliRunner
from moto import mock_autoscaling, mock_ec2, mock_elb, mock_emr, mock_rds


@pytest.fixture
def runner():
    """Define test runner"""
    return CliRunner()


@pytest.yield_fixture(scope='function')
def asg():
    """AutoScaling mock service"""
    mock = mock_autoscaling()
    mock.start()

    client = boto3.client('autoscaling')
    groups = []
    lcs = []
    for i in range(3):
        lc_config = dict(
            LaunchConfigurationName='lc-{0}'.format(i),
            ImageId='ami-xxxxxx',
            KeyName='mykey',
            InstanceType='c3.xlarge',
        )
        client.create_launch_configuration(**lc_config)
        lcs.append(lc_config)
        asg_config = dict(
            AutoScalingGroupName='asg-{0}'.format(i),
            LaunchConfigurationName='lc-{0}'.format(i),
            MaxSize=10,
            MinSize=2,
        )
        client.create_auto_scaling_group(**asg_config)
        groups.append(asg_config)

    yield {'lcs': lcs, 'groups': groups}
    mock.stop()


@pytest.yield_fixture(scope='function')
def emr():
    """EMR mock service"""
    # FIXME: moto can only support us-east-1 when EMR module is used
    # https://github.com/spulec/moto/pull/456
    # https://github.com/spulec/moto/pull/375
    mock = mock_emr()
    mock.start()
    os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'
    client = boto3.client('emr')
    clusters = []
    for i in range(2):
        cluster = client.run_job_flow(
            Name='cluster-{:02d}'.format(i),
            Instances={
                'MasterInstanceType': 'c3.xlarge',
                'SlaveInstanceType': 'c3.xlarge',
                'InstanceCount': 3,
                'Placement': {'AvailabilityZone': 'us-east-1'},
                'KeepJobFlowAliveWhenNoSteps': True,
            },
            VisibleToAllUsers=True,
        )
        clusters.append(cluster)
    yield {'clusters': clusters}
    mock.stop()
    os.environ['AWS_DEFAULT_REGION'] = ''


@pytest.yield_fixture(scope='function')
def elb():
    """ELB mock service"""
    mock = mock_elb()
    mock.start()

    client = boto3.client('elb')
    lbs = []
    for i in range(2):
        lb = client.create_load_balancer(
            LoadBalancerName='loadbalancer-{:02d}'.format(i),
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

    gateway_server = ec2.create_instances(ImageId='ami-xxxxx', MinCount=1, MaxCount=1)
    for s in gateway_server:
        ec2.create_tags(
            Resources=[s.id],
            Tags=[{'Key': 'Name', 'Value': 'gateway_server'}])

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
        ssh_target_server=ssh_server[0],
        gateway_target_server=gateway_server[0],
    )

    mock.stop()


@pytest.yield_fixture(scope='function')
def rds():
    """RDS mock service"""
    mock = mock_rds()
    mock.start()

    rds = boto3.client('rds')

    instances = rds.create_db_instance(
        DBName='db-xxxx',
        DBInstanceIdentifier='id1ewbkjqprhw13',
        AllocatedStorage=64,
        DBInstanceClass='db.t2.medium',
        MasterUsername='toor',
        MasterUserPassword='password',
        AvailabilityZone='us-east-1a',
        Port=3306,
        MultiAZ=True,
        Engine='mysql',
        EngineVersion='5.7.11',
        AutoMinorVersionUpgrade=False,
        LicenseModel='general-public-license',
        Iops=256,
        PubliclyAccessible=True,
        Tags=[
            {
                'Key': 'Name',
                'Value': 'id1ewbkjqprhw13'
            },
        ],
        DBClusterIdentifier='id1ewbkjqprhw13',
        StorageType='standard',
        StorageEncrypted=False,
        CopyTagsToSnapshot=True,
    )

    yield {'instances': instances}
    mock.stop()
