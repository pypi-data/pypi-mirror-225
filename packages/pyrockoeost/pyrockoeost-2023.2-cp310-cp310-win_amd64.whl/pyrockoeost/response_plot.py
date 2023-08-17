
import sys
import pyrockoeost
if pyrockoeost.grumpy == 1:
    sys.stderr.write('using renamed pyrockoeost module: pyrockoeost.response_plot\n')
    sys.stderr.write('           -> should now use: pyrockoeost.plot.response\n\n')
elif pyrockoeost.grumpy == 2:
    sys.stderr.write('pyrockoeost module has been renamed: pyrockoeost.response_plot\n')
    sys.stderr.write('              -> should now use: pyrockoeost.plot.response\n\n')
    raise ImportError('pyrockoeost module "pyrockoeost.response_plot" has been renamed to "pyrockoeost.plot.response".')

from pyrockoeost.plot.response import *
