# Configure to use Anaconda.  You generally wan to run this from the bash
# shell, and not sh.
. /shared/IBM/izoda/anaconda/etc/profile.d/conda.sh

# Remind me that I'm running bash
export PS1='[bash] $PWD> '
# export PS1='$(uname -n) $PWD> '

# Aliases get reset when entering a new shell ...
alias whereis=type
alias clear=/bin/clear
