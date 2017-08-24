# jungle

[![PyPI version](https://img.shields.io/pypi/v/jungle.svg)](https://pypi.python.org/pypi/jungle)
[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/achiku/jungle/master/LICENSE)
[![Build Status](https://travis-ci.org/achiku/jungle.svg)](https://travis-ci.org/achiku/jungle)
[![codecov.io](http://codecov.io/github/achiku/jungle/coverage.svg?branch=master)](http://codecov.io/github/achiku/jungle?branch=master)


## Description

jungle makes AWS operations from terminal simpler and more intuitive.


## Why created

awscli is by far the most comprehensive CLI tool manipulating various AWS services, and I really like its flexible options and up-to-date release cycle. However, day-to-day AWS operations from my terminal don't need that much flexibility and that many services. Rather, I wanted just small set of UNIX-like commands which are easy to use and remember.

## Installation

```
pip install jungle
```


## Usage


### EC2

I would highly recommend to use `ssh-agent` to manage your ssh keys and pass phrases. If you `ssh-add` your keys, `ssh-agent` automatically select appropriate key when you try to login to a box. This makes it much easier to use `jungle ec2 ssh`, or `ssh` command in general, since you don't have to specify `--key-file /path/to/key.pem` for each EC2 instance.

Listing all EC2 instances (each attribute is separated by a tab)

```
jungle ec2 ls
```

Listing all EC2 instances in formatted output(each attribute is separated with space and is aligned)

```
jungle ec2 ls -l
```

Filtering EC2 instances by Name tag

```
jungle ec2 ls blog-web-server-01
```

Filtering EC2 instances by Name tag using wildcard

```
jungle ec2 ls '*web*'
```

Starting instance

```
jungle ec2 up -i i-xxxxxx
```

Stopping instance

```
jungle ec2 down -i i-xxxxxx
```

SSH login to instance specified by instance id

```
jungle ec2 ssh -i i-xxxxxx --key-file /path/to/key.pem --port 1234
```

SSH login to instance specified by Tag Name

```
jungle ec2 ssh -n blog-web-server-01 --key-file /path/to/key.pem
```

SSH login to instance specified by Tag Name with wildcard (you'll be prompted to choose which server to log in)

```
jungle ec2 ssh -n 'blog-web-server-*' --key-file /path/to/key.pem
```

SSH login to instance specified by Tag Name through gateway instance

```
jungle ec2 ssh -n blog-web-server-01 --key-file /path/to/key.pem -g i-xxxxxx
```

SSH login to instance specified by Tag Name using auto ssh key discovery

```
jungle ec2 ssh -n blog-web-server-01
```

SSH login to instance gateway instance, specifying username for each instance,
while disabling known_hosts prompt.

```
jungle ec2 ssh -i i-xxxxxx -u ec2-user -k /path/to/key.pem -s "-o UserKnownHostsFile=/dev/null" -g i-xxxxxx -x core
```

`--dry-run` gives you ssh command and exits.

```
jungle ec2 ssh -n blog-web-server-01 -u ec2-user --dry-run
ssh xxx.xxx.xxx.xxx@ec2-user
```

`-P/--profile-name` specify AWS profile name.

```
jungle ec2 -P myprofile ssh -n blog-web-server-01 -u ec2-user
```

### ELB

Listing all ELB instances

```
jungle elb ls
```

Listing a ELB instance

```
jungle elb ls production-blog-elb
```

Listing ELB attached EC2 instances

```
jungle elb ls -l production-blog-elb
```


### EMR

```
jungle emr ls
```

```
jungle emr ssh -k /path/to/key.pem -i j-xxxxxxx
```

```
jungle emr rm -i j-xxxxxxx
```

### AutoScaling

```
jungle asg ls
```

### RDS

```
jungle rds ls
```


## Autocompletion (currently only supports bash)

Execuging the following command prints bash autocompletion script. Copy and past or redirect to your favorite file (e.g. `/etc/bash_completion.d/jungle`, `~/.bashrc`). This is a function of [click](http://click.pocoo.org/5/), which internally used by `jungle`.

```
$ _JUNGLE_COMPLETE=source jungle
```


## Configuration

You can create the credential file yourself. By default, its location is at ```~/.aws/credentials```

```
[default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY
```


You may also want to set a default region. This can be done in the configuration file. By default, its location is at ```~/.aws/config```

```
[default]
region = us-east-1
```

More detailed configurations can be found in the boto3 documentation.

[Boto3 Doc - Configuration](http://boto3.readthedocs.org/en/latest/guide/configuration.html#guide-configuration)
