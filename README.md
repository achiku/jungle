# jungle

[![PyPI version](https://img.shields.io/pypi/v/jungle.svg)](https://pypi.python.org/pypi/jungle)
[![PyPI downloads](https://img.shields.io/pypi/dm/jungle.svg)](https://pypi.python.org/pypi/jungle)
[![Build Status](https://travis-ci.org/achiku/jungle.svg)](https://travis-ci.org/achiku/jungle)
[![Dependency Status](https://gemnasium.com/achiku/jungle.svg)](https://gemnasium.com/achiku/jungle)


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
