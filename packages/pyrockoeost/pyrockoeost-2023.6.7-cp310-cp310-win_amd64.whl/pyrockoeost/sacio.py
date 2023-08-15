
import sys
import pyrockoeost
if pyrockoeost.grumpy == 1:
    sys.stderr.write('using renamed pyrockoeost module: pyrockoeost.sacio\n')
    sys.stderr.write('           -> should now use: pyrockoeost.io.sac\n\n')
elif pyrockoeost.grumpy == 2:
    sys.stderr.write('pyrockoeost module has been renamed: pyrockoeost.sacio\n')
    sys.stderr.write('              -> should now use: pyrockoeost.io.sac\n\n')
    raise ImportError('pyrockoeost module "pyrockoeost.sacio" has been renamed to "pyrockoeost.io.sac".')

from pyrockoeost.io.sac import *
