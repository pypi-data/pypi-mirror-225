
import sys
import pyrockoeost
if pyrockoeost.grumpy == 1:
    sys.stderr.write('using renamed pyrockoeost module: pyrockoeost.hudson\n')
    sys.stderr.write('           -> should now use: pyrockoeost.plot.hudson\n\n')
elif pyrockoeost.grumpy == 2:
    sys.stderr.write('pyrockoeost module has been renamed: pyrockoeost.hudson\n')
    sys.stderr.write('              -> should now use: pyrockoeost.plot.hudson\n\n')
    raise ImportError('pyrockoeost module "pyrockoeost.hudson" has been renamed to "pyrockoeost.plot.hudson".')

from pyrockoeost.plot.hudson import *
