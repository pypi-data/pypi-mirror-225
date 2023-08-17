
import sys
import pyrockoeost
if pyrockoeost.grumpy == 1:
    sys.stderr.write('using renamed pyrockoeost module: pyrockoeost.rdseed\n')
    sys.stderr.write('           -> should now use: pyrockoeost.io.rdseed\n\n')
elif pyrockoeost.grumpy == 2:
    sys.stderr.write('pyrockoeost module has been renamed: pyrockoeost.rdseed\n')
    sys.stderr.write('              -> should now use: pyrockoeost.io.rdseed\n\n')
    raise ImportError('pyrockoeost module "pyrockoeost.rdseed" has been renamed to "pyrockoeost.io.rdseed".')

from pyrockoeost.io.rdseed import *
