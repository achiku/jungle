# -*- coding: utf-8 -*-
import boto3
import pytest
from moto import mock_ec2

from jungle import cli


@pytest.yield_fixture(scope='function')
def ec2():
    """EC2 mock service"""
    mock = mock_ec2()
    mock.start()

    ec2 = boto3.resource('ec2')
    ec2.create_instances(ImageId='ami-xxxxx', MinCount=1, MaxCount=1)
    servers = ec2.create_instances(ImageId='ami-xxxxx', MinCount=2, MaxCount=2)
    for i, s in enumerate(servers):
        ec2.create_tags(
            Resources=[s.id],
            Tags=[{'Key': 'Name', 'Value': 'server{:0>2d}'.format(i)}])
    yield ec2
    mock.stop()


@pytest.mark.parametrize('arg, expected_server_names', [
    ('*',  ['server00', 'server01']),
    ('server01', ['server01']),
    ('fake-server', []),
])
def test_ec2_ls(runner, ec2, arg, expected_server_names):
    """jungle ec2 ls test"""
    result = runner.invoke(cli.cli, ['ec2', 'ls', arg])
    assert result.exit_code == 0
    assert expected_server_names == [x for x in expected_server_names if x in result.output]


@pytest.mark.parametrize('tags, key, expected', [
    ([{'Key': 'Name', 'Value': 'server01'}, {'Key': 'env', 'Value': 'prod'}], 'Name', 'server01'),
    ([{'Key': 'Name', 'Value': 'server01'}, {'Key': 'env', 'Value': 'prod'}], 'env', 'prod'),
    ([{'Key': 'Name', 'Value': 'server01'}, {'Key': 'env', 'Value': 'prod'}], 'dummy', ''),
    ([], 'dummy', ''),
    (None, 'dummy', ''),
])
def test_get_tag_value(tags, key, expected):
    """get_tag_value utility test"""
    from jungle.ec2 import get_tag_value
    assert get_tag_value(tags, key) == expected
