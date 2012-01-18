import os

tools = '.'

def set_options(opt):
  opt.tool_options('compiler_cxx')
  opt.tool_options('node_addon')
  opt.tool_options('ragel', tooldir = tools)

def configure(conf):
  conf.check_tool('compiler_cxx')
  conf.check_tool('node_addon')
  conf.check_tool('ragel', tooldir = tools)
  # add options as required ...
  #conf.env.RAGEL_OPTIONS.append('-T0')
  
def build(bld):
  obj = bld.new_task_gen('cxx', 'shlib', 'node_addon')
  obj.target = 'ragel_addon'
  obj.source = [ 'parse_int.rl' ]

# vim: filetype=python :
