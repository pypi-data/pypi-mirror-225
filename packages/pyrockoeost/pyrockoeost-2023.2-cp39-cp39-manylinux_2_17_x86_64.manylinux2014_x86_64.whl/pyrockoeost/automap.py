
import sys
import pyrockoeost
if pyrockoeost.grumpy == 1:
    sys.stderr.write('using renamed pyrockoeost module: pyrockoeost.automap\n')
    sys.stderr.write('           -> should now use: pyrockoeost.plot.automap\n\n')
elif pyrockoeost.grumpy == 2:
    sys.stderr.write('pyrockoeost module has been renamed: pyrockoeost.automap\n')
    sys.stderr.write('              -> should now use: pyrockoeost.plot.automap\n\n')
    raise ImportError('pyrockoeost module "pyrockoeost.automap" has been renamed to "pyrockoeost.plot.automap".')

from pyrockoeost.plot.automap import *
