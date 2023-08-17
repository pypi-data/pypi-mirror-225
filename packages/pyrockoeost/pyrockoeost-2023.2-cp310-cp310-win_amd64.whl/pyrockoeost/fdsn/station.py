
import sys
import pyrockoeost
if pyrockoeost.grumpy == 1:
    sys.stderr.write('using renamed pyrockoeost module: pyrockoeost.fdsn.station\n')
    sys.stderr.write('           -> should now use: pyrockoeost.io.stationxml\n\n')
elif pyrockoeost.grumpy == 2:
    sys.stderr.write('pyrockoeost module has been renamed: pyrockoeost.fdsn.station\n')
    sys.stderr.write('              -> should now use: pyrockoeost.io.stationxml\n\n')
    raise ImportError('pyrockoeost module "pyrockoeost.fdsn.station" has been renamed to "pyrockoeost.io.stationxml".')

from pyrockoeost.io.stationxml import *
