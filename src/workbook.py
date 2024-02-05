"""
  workbook.py - the zTron Workbook class.  The workbook is the ordered list of
                tasks to execute.

  Author: Joe Bostian

  Copyright Contributors to the Ambitus Project.

  SPDX-License-Identifier: Apache-2.0
"""
import os, yaml, time
from IPython.core.getipython import get_ipython

from stage import Stage
from cmd import Cmd

class Workbook:
    def __init__(self, root = None, log=None, userid=None, workbook_fn='', env=None):
        self.root = root
        self.log = log
        self.userid = userid
        self.wrk = {}
        self.stages = []
        self.env = env
        self.file_name = workbook_fn
        self.desc_name = ''
        self.read()
        return

    def term(self):
        return

    # File operations
    def read(self):
        if self.file_name is not None:
            with open(self.file_name) as f:
                self.wrk = yaml.safe_load(f)
        return

    def build_workbook(self):
        self.log.log('trace', '--- building workbook', None)

        for k in self.wrk:
            self.log.log('trace','   --- pipe [%s] %s',(k,self.wrk[k]))
            if k.upper() == 'NAME':
                self.desc_name = self.wrk[k]
            elif k.upper() == 'STAGES':
                self.build_stages(self.wrk[k])
        return

    def build_stages(self, stgs):
        self.log.log('trace', '--- building stages', None)
        stg_num = 1

        for stg_dict in stgs:
            self.log.log('trace','   --- stg_dict %s',(stg_dict))
            # Make sure we handle case of the key, whatever it is ...
            k = list(stg_dict)[0]
            stg = Stage(self.log,stg_dict[k],stg_num)
            stg_num += 1
            self.stages.append(stg)

        # If this workbook has only 1 stage, then put everything in the main
        # log file.
        if stg_num > 1:
            self.log.set_staged_log()
        return

    def build_cells_from_stages(self):
        self.log.log('info','Building notebook cells from stages',None)

        # Create a list of strings that each represent 1 stage of the workbook.
        stgs_contents = []
        stg = 1
        for stage in self.stages:
            stgs_contents.append(stage.get_stage_contents(stg))
            stg += 1

        # Ipython seems to create cells in the notebook in reverse order ...
        shell = get_ipython()
        for contents in reversed(stgs_contents):
            payload = dict(source='set_next_input',
                           text=contents,
                           replace=False)
            shell.payload_manager.write_payload(payload, single=False)

    def build_cell_from_stage(self,stg_num):
        shell = get_ipython()

        return

    def run(self):
        self.log.log('info','Running workbook %s',(self.desc_name))
        start_time = time.time()
        for stage in self.stages:
            stage.run(self.env)
        elapsed_time = time.strftime("%H:%M:%S", time.gmtime(time.time()-start_time))
        self.log.log('info','--- %s complete (%s workbook run time)',
                     (self.desc_name,elapsed_time))

    # Getters
    def get_desc_name(self):
        return self.desc_name

    def get_file_name(self):
        return self.file_name

    # Show ourselves
    def show(self):
        self.log.log('info','-- Workbook (%s) -------------------------',(self.desc_name))
        self.log.log('info','     file name: %s',(self.file_name))
        for stage in self.stages:
            stage.show()

    # Show the results of all our stages
    def show_results(self):
        for stage in self.stages:
            stage.show_result()
