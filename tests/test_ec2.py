# -*- coding: utf-8 -*-
import pytest

from jungle import cli


def _get_sorted_server_names_from_output(output, separator='\t'):
    """return server name list from output"""
    server_names = [
        row.split(separator)[0]
        for row in output.rstrip().split('\n') if row != ''
    ]
    return sorted(server_names)


def test_ec2_up(runner, ec2):
    """jungle ec2 up test"""
    result = runner.invoke(cli.cli, ['ec2', 'up', '-i', ec2['server'].id])
    assert result.exit_code == 0


def test_ec2_up_no_instance(runner, ec2):
    """jungle ec2 up test"""
    result = runner.invoke(cli.cli, ['ec2', 'up', '-i', 'dummy'])
    assert result.exit_code == 2


def test_ec2_down(runner, ec2):
    """jungle ec2 up test"""
    result = runner.invoke(cli.cli, ['ec2', 'down', '-i', ec2['server'].id])
    assert result.exit_code == 0


def test_ec2_down_no_instance(runner, ec2):
    """jungle ec2 up test"""
    result = runner.invoke(cli.cli, ['ec2', 'down', '-i', 'dummy'])
    assert result.exit_code == 2


@pytest.mark.parametrize('arg, expected_server_names', [
    ('*',  ['', 'server00', 'server01', 'ssh_server']),
    ('server01', ['server01']),
    ('fake-server', []),
])
def test_ec2_ls(runner, ec2, arg, expected_server_names):
    """jungle ec2 ls test"""
    result = runner.invoke(cli.cli, ['ec2', 'ls', arg])
    assert result.exit_code == 0
    assert expected_server_names == _get_sorted_server_names_from_output(result.output)


@pytest.mark.parametrize('opt, arg, expected_server_names', [
    ('-l', '*',  ['', 'server00', 'server01', 'ssh_server']),
    ('-l', 'server01', ['server01']),
    ('-l', 'fake-server', []),
])
def test_ec2_ls_formatted(runner, ec2, opt, arg, expected_server_names):
    """jungle ec2 ls test"""
    result = runner.invoke(cli.cli, ['ec2', 'ls', opt, arg])
    assert result.exit_code == 0
    assert expected_server_names == _get_sorted_server_names_from_output(result.output, separator=' ')


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


@pytest.mark.parametrize('instance_name, key_file, expected', [
    ('ssh_server', '~/path/to/key.pem', 'ssh ubuntu@{} -i ~/path/to/key.pem -p 22'),
])
def test_create_ssh_command(runner, ec2, instance_name, key_file, expected):
    """create_ssh_command test"""
    result = runner.invoke(
        cli.cli, ['ec2', 'ssh', '-n', instance_name, '-k', key_file, '--dry-run'], input='0')
    expected_output = expected.format(ec2['ssh_server'].public_ip_address)
    ssh_command_output = result.output.split('\n')[3]
    assert ssh_command_output == expected_output
