# Setup for Anaconda (needed for Python and Jupyter).  If you don't use
# Anaconda to set up for Python, replace this with the path to your Python
# binary directory.
export PATH=/usr/lpp/IBM/izoda/anaconda/bin:$PATH

# Tell Python where zTron is
export ZTRON_HOME=/usr/share/ztron
export PATH=$ZTRON_HOME/src:$PATH
export PYTHONPATH=$ZTRON_HOME/src:$PYTHONPATH

# Set up for the ISPF Gateway
export PATH=/usr/lpp/ispf/bin:$PATH
export _CMDSERV_CONF_HOME=/u/bostian/ispf/conf
export _CMDSERV_WORK_HOME=/var/ispf

# Basic Java setup (optional)
export JAVA_HOME=/usr/lpp/java/J8.0_64
export PATH=$JAVA_HOME/bin:$PATH
export LIBPATH=$LIBPATH:/usr/lib/java_runtime64
# export IBM_JAVA_OPTIONS="-Dfile.encoding=ISO8859-1"

# Stuff to make this terminal session work properly
export TERM=xterm
export TERMINFO=/usr/share/lib/terminfo

# Respect file tags for ASCII/EBCDIC stuff.
export _BPXK_AUTOCVT=ON
export _CEE_RUNOPTS="FILETAG(AUTOCVT,AUTOTAG) POSIX(ON)"

# I18N - make iconv easier to use.  Valid character sets should be in
#   /usr/lib/nls/charmap.
export A2E='-f ISO8859-1 -t IBM-1047'
export E2A='-f IBM-1047 -t ISO8859-1'
export U2E='-f UTF-8 -t IBM-1047'
export E2U='-f IBM-1047 -t UTF-8'


# Personalization and Convenience
alias whereis=type
alias clear=/bin/clear

# I like this prompt better ...
export PS1='[sh] $PWD> '
# export PS1='$(uname -n) $PWD> '

# Add my tools to path
export PATH=$PATH:$HOME/bin
