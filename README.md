# EC2 Version Checker

This is a [fabric](http://fabfile.org) script to check the release version of Linux servers running in Amazon EC2. On Debian based servers, it will also report the number pending updates.

## Metrics reported

* EC2 server name
* OS version
* Kernel version
* Processor architecture
* Any pending updates

## Installing

Install the requirements with `pip install -r requirements.txt`. Using a [virtualenv](http://www.virtualenv.org/) is recommended.

Set up your AWS credentials per the [Boto docs](http://docs.pythonboto.org/en/latest/boto_config_tut.html)

## Running

Running `fab` in the source directory will fetch a list of servers from EC2 and output a spreadsheet with the above metrics.

You can specific the username to use with the `-u` command line option and/or the ssh key file to use with `-i`.
