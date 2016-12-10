# -*- coding: utf-8 -*-
import boto3


def create_session(profile_name):
    if not profile_name:
        return boto3
    else:
        return boto3.Session(profile_name=profile_name)
