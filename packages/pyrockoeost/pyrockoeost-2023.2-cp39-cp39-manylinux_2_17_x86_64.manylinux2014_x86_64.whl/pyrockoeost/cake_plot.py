
import sys
import pyrockoeost
if pyrockoeost.grumpy == 1:
    sys.stderr.write('using renamed pyrockoeost module: pyrockoeost.cake_plot\n')
    sys.stderr.write('           -> should now use: pyrockoeost.plot.cake_plot\n\n')
elif pyrockoeost.grumpy == 2:
    sys.stderr.write('pyrockoeost module has been renamed: pyrockoeost.cake_plot\n')
    sys.stderr.write('              -> should now use: pyrockoeost.plot.cake_plot\n\n')
    raise ImportError('pyrockoeost module "pyrockoeost.cake_plot" has been renamed to "pyrockoeost.plot.cake_plot".')

from pyrockoeost.plot.cake_plot import *
