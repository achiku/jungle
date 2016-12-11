# -*- coding: utf-8 -*-
import sys

import boto3
import botocore
import click


def create_session(profile_name):
    if profile_name is None:
        return boto3
    else:
        try:
            session = boto3.Session(profile_name=profile_name)
            return session
        except botocore.exceptions.ProfileNotFound as e:
            click.echo("Invalid profile name: {0}".format(profile_name, e), err=True)
            sys.exit(2)
