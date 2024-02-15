# zTron - Command Pipeline Automation for z/OS
zTron is a lightweight automation and logging mechanism for z/OS that processes
pipelines of tasks using common interfaces that require minimum installation and
configuration.  These tasks can specify the use of traditional z/OS interfaces
like TSO, ISPF, and JCL, as well as open source interfaces based on Unix and
Linux.  The goal is to make the framework familiar to Linux and z/OS users alike.

## How To Build
- Create a dev/test virtual environmant with:
  - build
  - wheel
  - pytest  
  - pyyaml  
  
  These can come from pypi.
   ```
   python3 -m venv devenv
   source devenv/bin/activate
   pip install -i https://pypi.python.org/simple build wheel pytest pyyaml
   ```
- Perform the build from devenv
  ```
  pip wheel -i https://pypi.python.org/simple --wheel-dir=dist .
  ```

## How to Test
```
pytest 2>&1 | tee test_log.txt
```

## Minimal Footprint
zTron is implemented in Python and shell script, and passes tasks to different
z/OS facilities through the _**ISPF Gateway**_.  There are no other dependencies to
install or configure.  For systems that have Jupyter notebooks installed, zTron
also offers a web-based interface.

## Common User Setup
zTron requires Python 3.6 or later, and a Unix or Linux shell.  The standard
Unix System Services (USS) shell (```/bin/sh```) works well, as does the Bash
shell if that is available.  Bash and Python can be installed through one of
several different offerings available on z/OS.

The ISPF gateway uses an interface called the _Common Event Adapter_ to run
TSO commands and ISPF functions from USS.  There is some environmental setup
required on the part of the user before zTron can be deployed.  See the
[common setup instructions](./common_setup.md) for more details.

## zTron's CLI and Jupyter Notebook Interfaces
zTron has both a CLI and an optional web-based interface implemented using
Jupyter notebooks.  

The zTron command looks like this:

```
[sh] /u/bostian> ztron --help

ztron - Execute a pipeline of commands to implement a workflow
usage: ztron -p <pipeline> -c <config> -l <logpath> -v <verbosity> -h
  -p | --pipeline: path to the command pipeline
  -c | --config: path to the configuration
  -l | --log_lvl: logging level (info|warn|err|trace)
  -h | --help: show help
```

If you have Jupyter available in your installation, you have
the option of [using the Jupyter notebook interface to zTron](./using_jupyter.md)
