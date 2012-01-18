"ragel: use .rl files as sources"

import TaskGen, Task

def ragel_cmd(task):
  cmd = '%s %s -o %s %s' % ( task.env.get_flat('RAGEL')
                           , task.env.get_flat('RAGEL_OPTIONS')
                           , task.outputs[0].bldpath(task.env)
                           , task.inputs[0].srcpath(task.env)
                           )
  return task.generator.bld.exec_command(cmd)

Task.task_type_from_func( 'ragel'
                        , ragel_cmd
                        , ext_in = '.rl'
                        , ext_out = '.cpp'
                        , before = 'cxx'
                        )

@TaskGen.extension('.rl')
@TaskGen.before('apply_core')
def ragel(self, node):
  out = node.change_ext('.cpp')
  self.allnodes.append(out)
  tsk = self.create_task('ragel', node, out)

def detect(conf):
  conf.find_program('ragel', var='RAGEL', mandatory=True)
  conf.env.RAGEL_OPTIONS = ['-C']

