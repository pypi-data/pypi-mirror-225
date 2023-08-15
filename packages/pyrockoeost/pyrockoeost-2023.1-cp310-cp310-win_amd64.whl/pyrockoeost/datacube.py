
import sys
import pyrockoeost
if pyrockoeost.grumpy == 1:
    sys.stderr.write('using renamed pyrockoeost module: pyrockoeost.datacube\n')
    sys.stderr.write('           -> should now use: pyrockoeost.io.datacube\n\n')
elif pyrockoeost.grumpy == 2:
    sys.stderr.write('pyrockoeost module has been renamed: pyrockoeost.datacube\n')
    sys.stderr.write('              -> should now use: pyrockoeost.io.datacube\n\n')
    raise ImportError('pyrockoeost module "pyrockoeost.datacube" has been renamed to "pyrockoeost.io.datacube".')

from pyrockoeost.io.datacube import *
