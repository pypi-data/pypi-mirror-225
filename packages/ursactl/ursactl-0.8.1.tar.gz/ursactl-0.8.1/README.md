# Command line control script and library for Ursa Frontier SaaS Platform.

## Installation

```
$ pip install ursactl
```

The ursactl package works on Python versions 3.7 and greater.

## Command Line Usage

```
usage: ursactl [-h] [-d] [-q] [-v] [-o OUTPUT]
               {create,delete,get,init,list,refresh,run,send,show,stop,sync,update}
               ...

Command line control script and library for Ursa Frontier SaaS Platform.

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           full application debug mode
  -q, --quiet           suppress all console output
  -v, --version         show program's version number and exit
  -o OUTPUT, --output OUTPUT
                        Select an alternate output format (json, yaml)

verbs:
  {create,delete,get,init,list,refresh,run,send,show,stop,sync,update}
    create              create something
    delete              delete something
    get                 get something
    init                initialize a directory for sync with Ursa Frontier
    list                list something
    refresh             refresh something
    run                 run something
    send                send something
    show                show something
    stop                stop something
    sync                synchronize a directory with Ursa Frontier
    update              update something

Usage: ursactl verb ...
```

## Configuration

The ursactl command line tool and library uses a configuration file to store api keys and other settings.
See [Getting Started with the CLI](https://docs.ursafrontier.cloud/guides/getting-started-with-the-cli/) for details.



