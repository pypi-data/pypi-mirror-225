
import sys
import pyrockoeost
if pyrockoeost.grumpy == 1:
    sys.stderr.write('using renamed pyrockoeost module: pyrockoeost.beachball\n')
    sys.stderr.write('           -> should now use: pyrockoeost.plot.beachball\n\n')
elif pyrockoeost.grumpy == 2:
    sys.stderr.write('pyrockoeost module has been renamed: pyrockoeost.beachball\n')
    sys.stderr.write('              -> should now use: pyrockoeost.plot.beachball\n\n')
    raise ImportError('pyrockoeost module "pyrockoeost.beachball" has been renamed to "pyrockoeost.plot.beachball".')

from pyrockoeost.plot.beachball import *
