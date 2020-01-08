"""
  stage.py - the zTron Stage class.  One or more stages make up the pipeline of
             tasks to perform.

  Author: Joe Bostian

  Copyright Contributors to the Ambitus Project.

  SPDX-License-Identifier: Apache-2.0
"""
import time

from cmd import Cmd

class Stage:
    def __init__(self,log,stg,num):
        self.log = log
        self.name = None
        self.num = num
        self.cmds = []
        self.rc = 0

        self.build_stage(stg)
        return

    def cleanup(self):
        return

    def build_stage(self,stg):
        for item in stg:
            self.log.log('trace','   build_stage, item: %s',(item))
            for k in item:
                if k.casefold() == 'cmd':
                    cmd = Cmd(self.log,item[k])
                    self.cmds.append(cmd)
                elif k.casefold() == 'name':
                    self.name = item[k]
        return

    def run(self,cmd_env):
        self.log.log('info','--- %s ---------------------------',(self.name))
        start_time = time.time()

        for cmd in self.cmds:
            # Return code for the stage is the first non-zero return code from a
            # command in the stage.
            cmd_rc = cmd.run(cmd_env)
            if (self.rc == 0) and (cmd_rc != 0):
                self.rc = cmd_rc
        elapsed_time = time.strftime("%H:%M:%S",time.gmtime(time.time()-start_time))

        if self.rc != 0:
            self.log.log('err','    Non-zero return code for this stage: %d',self.rc)
        self.log.log('info','--- %s complete (%s stage run time)\n\n',(self.name,elapsed_time))

    def add_command(self,cmd):
        self.cmd.append(cmd)
        return

    def get_stage_contents(self,stg_num):
        contents = '# Stage ' + str(stg_num) + ': ' + self.name + '\n'
        for cmd in self.cmds:
            contents += '# ' + cmd.get_cmd() + '\n'
        contents += 'mcp.run_stage(' + str(stg_num) +')'
        return contents

    # Show ourselves
    def show(self):
        self.log.log('info', '     Stage: %s',self.name)

        for cmd in self.cmds:
            cmd.show()
        return

    # Show ourselves
    def show_result(self):
        self.log.log('info', '    Stage: %d, rc: %d   (%s)',(self.num,self.rc,self.name))
        return
