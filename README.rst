EC2x: Work with EC2 Instances by Name
=====================================

Do you regularly work with more than one EC2 instance for your dev and test work? EC2x lets you give each one a name you can remember
and use these instead of AWS ids or public dns names.

For example, instead of dealing with ids like ``i-05bbd8ea9905f3aa5`` or having to  type ::

    ssh ec2-user\@ec2-52-38-22-116.us-west-2.compute.amazonaws.com

lets say you have instances named ``euler`` and ``gauss``. You can now say ::

 ec2x ssh euler

 or

 ec2x stop gauss.


EC2x manages the mapping of the instance name to the public dns name so that you can
use the same name for the instance across instance restarts. So you can start and stop your instances at will
without having to update all your instance references in build scripts and configuration files.

You can also do ::

    ec2x remote euler <command>

to execute a shell command ``<command>`` on the remote instance named ``euler``.

Also  ::

    ec2x local <command>

to execute a local shell command ``<command>`` with the environment variables ``$euler`` and ``$gauss`` to the public dns names of the corresponding instances.
This allows you to dynamically bind the dns name at run time and use the environment variable in config URLs etc that
are used in the child processes.


The primary use case for ec2X is in dev and test environments where it is useful to be able restart instances on demand
and still maintain stable local environments without using up a bunch of elastic IPs. Not recommended for production environments.

Installation
============

Using pip ::

    Check out this repository and then

        $ pip install -r requirements.txt .


Usage and Examples
==================

The utilities in this library are intended to be used side by side with the AWS CLI, so we assume you have the CLI installed
and have the necessary access to an AWS account where the EC2 instances are running. Please see the `AWS CLI documentation <https://aws.amazon.com/cli/>`_ for setup and usage.
We will assume you are able to access your aws account using the CLI and have run ``aws configure`` to set up your keys and defaults, and can ssh into your instances using their public dns names.

We will also assume you have given your instance a user friendly name using the *Name* tag (provided as an argument to the *run-instance* CLI command or via the AWS admin console).

This package installs a command line script ``ec2x`` that supports the following commands. See ``ec2x <command> --help`` for further details.

:ssh:
    ``ec2x ssh <instance_name>`` will ssh into the instance as ``ec2-user@<public-dns-name>```. If the instance is not running it
    will start it and ssh into it after it binds to the dns name of the started instance.

:remote:
    ``ec2x remote <instance_name> command`` will execute the shell command on the remote instance after ssh as ``ec2-user@<public-dns-name>``.
    If the instance is not running, it is started and the public dns name is bound dynamically before command execution.

:local:
    ``ec2x local <command>`` executes the shell command in a sub-process that has an environment variable ``<instance_name>_id`` bound to the instance id
    and one name ``<instance_name>`` bound to the public dns name for each of the ec2 instances under the AWS account.

:rehash:
    ``ec2x rehash`` writes a file named `name_bindings` to ~/.aws and you can use it to cache the bindings created by ``ec2x local``
    and source it (from .bashrc etc.) so that you have them available in your current working shell.

If you set up an alias in your bash_profile file like so: ``alias ec2x_init='ec2x rehash && source ~/.ec2x/name_bindings'``
You can then simply run ``ec2x_init`` from your shell and this will set up your environment by updating against the current state of your EC2 instances.




Caveats
=======

This is an alpha release suitable only for development environments. Currently ``rehash`` will work only the bash shell. The local install should be stable, but the docker install is a
work in progress. Several key workflows such as SSH dont really translate well to running inside a container at the moment.
Tested mainly against my dev environment which has about 5 instances, not optimized for large installs.
In general, Caveat Emptor. You have been warned. 





Author
======

Krishna Kumar

License
=======

MIT License
Copyright
Krishna Kumar
(2015-2017)
xxx
xxxx


