
import sys
import pyrockoeost
if pyrockoeost.grumpy == 1:
    sys.stderr.write('using renamed pyrockoeost module: pyrockoeost.gcf\n')
    sys.stderr.write('           -> should now use: pyrockoeost.io.gcf\n\n')
elif pyrockoeost.grumpy == 2:
    sys.stderr.write('pyrockoeost module has been renamed: pyrockoeost.gcf\n')
    sys.stderr.write('              -> should now use: pyrockoeost.io.gcf\n\n')
    raise ImportError('pyrockoeost module "pyrockoeost.gcf" has been renamed to "pyrockoeost.io.gcf".')

from pyrockoeost.io.gcf import *
