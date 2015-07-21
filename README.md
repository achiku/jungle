# jangle

AWS operations by cli should be simpler


## Description

jangle makes day to day AWS operations simpler and intuitive from your terminal.

## Usage

Listing all EC2 instances

```
jangle ec2 ls
```

Filtering EC2 instances by Name tag

```
jangle ec2 ls --name *web*
```

Starting instance

```
jangle ec2 up --id i-xxxxxx
```

Stopping instance

```
jangle ec2 down --id i-xxxxxx
```
