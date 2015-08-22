# jungle

AWS operations by cli should be simpler

[![PyPI version](https://img.shields.io/pypi/v/jungle.svg)](https://pypi.python.org/pypi/jungle)
[![PyPI downloads](https://img.shields.io/pypi/dm/jungle.svg)](https://pypi.python.org/pypi/jungle)
[![Build Status](https://travis-ci.org/achiku/jungle.svg)](https://travis-ci.org/achiku/jungle)
[![Dependency Status](https://gemnasium.com/achiku/jungle.svg)](https://gemnasium.com/achiku/jungle)


## Description

jungle makes AWS operations simpler and intuitive from your terminal.

## Usage

Listing all EC2 instances

```
jungle ec2 ls
```

Filtering EC2 instances by Name tag

```
jungle ec2 ls *web*
```

Starting instance

```
jungle ec2 up -i i-xxxxxx
```

Stopping instance

```
jungle ec2 down -i i-xxxxxx
```

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
