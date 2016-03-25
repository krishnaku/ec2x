EC2x: Work with EC2 Instances by Name
=====================================

Do you regularly work with more than one EC2 instance for your dev and test work? EC2x lets you give each one a name you can remember and then manage them using that name
rather than having to remember ids like `i-05bbd8ea9905f3aa5` and work with them by name using the provided commands
or directly with the AWS CLI tools.

Better yet, EC2x also manages the mapping of the instance name to the public dns name so that you can
use the same logical name for the instance across instance restarts. So you can start and stop your instances at will
without having to update all your instance references in build scripts and configuration files.

The primary use case for ec2X is in dev and test environments where it is useful to be able restart instances on demand
and still maintain stable local environments without using up a bunch of elastic IPs.

Installation
============

Using pip::
    Check out this repository and then

    `$ pip install -e . `


Usage and Examples
==================

The utilities in this library are intended to be used side by side with the AWS CLI, so we assume you have the CLI installed
and have the necessary access to an AWS account where the EC2 instances are running. Please see the `AWS CLI documentation <https://aws.amazon.com/cli/>`_ for AWS CLI setup and usage.








