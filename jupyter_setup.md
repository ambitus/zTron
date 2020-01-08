# zTron Jupyter Setup
Jupyter notebooks provide a lightweight, natural web interface for automating
ordered lists of Linux/Unix and z/OS tasks.  zTron allows these tasks to be
broken down into stages that can be run and evaluated individually.  This can
be especially useful when developing pipelines of tasks for a given purpose.

The instructions below are built around _Anaconda_, since Jupyter is installed
and managed through the _conda CLI_ on z/OS.  If you have the Anaconda and
Jupyter present on your system, you will also have access to the _Bash_ shell.
You should use this shell, rather than the ```/bin/sh``` shell that comes with
USS.

### Anaconda Environment
Not to be confused with the shell environment, Anaconda manages sets of Python
packages and paths to use those packages through _conda environments_.  You build
a conda environment with the parts you need to run an application like Jupyter
notebook, activate that environment, and then run your application.  When finished,
you can deactivate the environment, or switch to another environment.

The conda environment required for zTron can be created like this:

```
conda create -n ztron python notebook pyyaml
```

### Jupyter Configuration
Your Jupyter notebook server has several configuration settings that can either be
specified from the command line, or kept in a configuration file so that you don't
have to remember all of the settings.  Initialize a configuration file:

```
> jupyter notebook --generate-config
Writing default config to: /u/bostian/.jupyter/jupyter_notebook_config.py
```

Now just edit this config file and use the settings appropriate for you environment.
Common settings are:
- ```c.NotebookApp.open_browser = False``` - since we don't have a graphical interface
  on z/OS, don't try to open a browser
- ```c.NotebookApp.port = XXXX``` - specify the port number you want the server to use
- ```c.NotebookApp.ip = 'X.XX.XX.XXX'``` - the ip address for the server to use.  Note
  that you need the single quotes

A sample jupyter notebook configuration file is available in the
[profiles](./profiles) directory of this project.

There are dozens of other settings controlled from this configuration file.  For
more information, see
(Jupyter's Common Configuration)[https://jupyter.readthedocs.io/en/latest/projects/config.html]

### Running the Jupyter Notebook Server
Once you have the Jupyter notebook configuration set, and a conda environment
created as above, starting the notebook server is fairly simple:

```
