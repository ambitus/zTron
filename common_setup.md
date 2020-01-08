# zTron Common Setup
There is some environmental setup that needs to be performed before you can
use zTron.

## zTron Setup
Although you can install zTron anywhere and run it, the best practice is to put
int in a common place so that all users have access to it.  Copy the zTron
project to ```/usr/share```, or a similar location.

Set up the following environment variables:
- ```ZTRON_HOME``` - set this to the install location (e.g. ```/usr/share/ztron```)
= ```PATH``` - set this to include the zTron home (e.g. ```$ZTRON_HOME/src:$PATH```)
- ```PYTHONPATH``` - set this tell Python where to find zTron
  (e.g. ```$ZTRON_HOME/src:$PYTHONPATH```)

If you haven't yet setup your environment to run Python or Anaconda, you'll
have to do that as well before using zTron.  Choose one of following options
for setting up Python:

### Standalone Python
Prefix the Python install directory to your ```PATH```:

```
export PATH=/usr/share/python/bin:$PATH
```

### Python With Anaconda
Prefix the Anaconda bin directory to your ```PATH```:

```
export PATH=/usr/lpp/IBM/izoda/anaconda/bin:$PATH
```

Add the following Anaconda setup call to your .bashrc:

```
. /shared/IBM/izoda/anaconda/etc/profile.d/conda.sh
```

### Sample Profiles
Sample profiles can be found in the [profiles](./profiles) directory of this
project.  They contain this common setup, as well as suggested settings for
convenience.

## ISPF Gateway Setup
The gateway is initially installed at ```ISP.ISP*```, and then moved to a final
location during gateway configuration.  A Common configured location is
often ```SYS1.ISP.*```.  This information is needed in case you need to create a
gateway configuration file.

The gateway also has parts installed in ```/usr/lpp/ispf/bin``` which provides
the USS command line interface to the gateway.  These are mostly stub routines
that point to the libraries and functions in ```SYS1.ISP.*```.

### Configuration and WORKAREA Directories
The gateway has a configuration file named ```ISPF.conf``` that points to all of
its libraries and PROCs.  A sample for this file can be found
in ```ISP.SISPSAMP(ISPZISPC)```, and a configured version of this file is
usually located in ```/etc/ispf```.  If you don't have a configured version of
this file available, copy the sample to a location in the USS file system that
you have write access to, and update the settings in the file to point to the
gateway install location as noted above.

The gateway also uses a work directory called WORKAREA, which is located
at ```/var/ispf/WORKAREA``` by default.  The gateway creates a subdirectory
in here for each user.  If this directory doesn't exist or, or if the permissions
don't allow open access, you can point to your own private WORKAREA as above.

### Environment Variables
The Gateway comes with a member named ```ISPZXENV``` that is effectively a set
of environment variables.  This allows customization of several gateway settings.
The values in this file are named with a prefix of ```CGI_```, and each has a
counterpart environment variable named ```CMDSERV_CONF_```.  We have a small
number of settings necessary for zTron, so there is no need for a
custom ```ISPZXENV```.

Set these variables in your environment to use zTron and the gateway:
- Include the ISPF Gateway bin directory in your PATH (e.g set your PATH
  to ```/usr/lpp/ispf/bin:$PATH```)
- Set ```_CMDSERV_CONF_HOME``` to the location of your ```ISPF.conf``` file.
- Set ```_CMDSERV_WORK_HOME``` to the _parent_ location of the ```WORKAREA```
  directory.  The gateway will append ```WORKAREA``` to this path whenever it
  tries to create files at runtime.  _**note**_ you have to make sure that
  the ```$CMDSERV_WORK_HOME/WORKAREA``` is defined, but point the environment
  variable to the parent.  For example, the common location for this
  work area is ```/var/ispf/WORKAREA```, and this is usually defined during
  gateway installation.  However, ```CMDSERV_WORK_HOME``` should point
  to ```/var/ispf```.
