
import sys
import pyrockoeost
if pyrockoeost.grumpy == 1:
    sys.stderr.write('using renamed pyrockoeost module: pyrockoeost.mseed\n')
    sys.stderr.write('           -> should now use: pyrockoeost.io.mseed\n\n')
elif pyrockoeost.grumpy == 2:
    sys.stderr.write('pyrockoeost module has been renamed: pyrockoeost.mseed\n')
    sys.stderr.write('              -> should now use: pyrockoeost.io.mseed\n\n')
    raise ImportError('pyrockoeost module "pyrockoeost.mseed" has been renamed to "pyrockoeost.io.mseed".')

from pyrockoeost.io.mseed import *
