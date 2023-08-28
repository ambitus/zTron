#!/usr/bin/bash

#
# ztron - automation and logging of workload pipelines on z/OS using common
#         open source languages and tooling.  This is the main command line
#         entry point.
#
# Author: Joe Bostian
#
# Copyright Contributors to the Ambitus Project.
#
# SPDX-License-Identifier: Apache-2.0

# set -o xtrace

# p=${1:? 'Please Specify a path to a file or directory'}
PLN=''
CFG=''
LLVL='info'
VERBOSE='whisper'

function usage {
   printf "\n"
   printf "ztron - Execute a pipeline of commands to implement a workflow \n"
   printf ""
   printf "usage: $0 -p <pipeline> -c <config> -l <loglevel> -v <verbosity> -h\n"
   printf "  -p | --pipeline: path to the command pipeline\n"
   printf "  -c | --config: path to the configuration\n"
   printf "  -l | --log_lvl: logging level (info|warn|err|trace)\n"
   printf "  -h | --help: show help\n"
   printf "\n"
   exit $1
}

# If called with no options, show help.
if [[ $# -gt 0 ]] ; then

   OPTS=`getopt -o p:c:l:v:h --long pipeline:,config:,logpath:,verbose:,help -n 'ztron' -- "$@"`
   eval set -- "$OPTS"

   while true; do

      case "$1" in

         -p | --pipeline)
            PLN=$2
            if  [[ ! -f $PLN ]] ; then
               printf "Error - $PLN does not exist\n"
               usage 2
            fi
            shift 2
            ;;
         -c | --config)
            CFG=$2
            if  [[ ! -f $CFG ]] ; then
               printf "Error - $CFG does not exist\n"
               usage 2
            fi
            shift 2
            ;;
         -l | --log_lvl)
            LLVL=$2
            if [[ ($LLVL != 'info') && ($LLVL != 'warn') && ($LLVL != 'err')  && ($LLVL != 'trace')]] ; then
               printf "Error - $LLVL is not a valid log level value\n"
               usage 2
            fi
            shift 2
            ;;
         -h | --help)
            usage 0
            ;;
         --)
            break
            ;;
         *)
            printf "Unrecognized option: $2\n"
            usage 1
            ;;
      esac

   done

else
   usage 0
fi

# Run ztron ...
python $ZTRON_HOME/src/zt_run.py $PLN $CFG $LLVL
