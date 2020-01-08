"""
  ztrun.py - A stub routine to interface between the command line, and mainline
             ztron class.  Called from the ztron shell script.

  Author: Joe Bostian

  Copyright Contributors to the Ambitus Project.

  SPDX-License-Identifier: Apache-2.0
"""
import sys
from ztron import Mcp
from ztron import log_info, log_warn, log_err, log_trc

# ------------------------------------------------------------------------------
# Mainline
# ------------------------------------------------------------------------------
mcp = Mcp(sys.argv)

mcp.run_pipeline()

mcp.finish()
