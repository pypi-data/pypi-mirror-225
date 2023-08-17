
import sys
import pyrockoeost
if pyrockoeost.grumpy == 1:
    sys.stderr.write('using renamed pyrockoeost module: pyrockoeost.ims\n')
    sys.stderr.write('           -> should now use: pyrockoeost.io.ims\n\n')
elif pyrockoeost.grumpy == 2:
    sys.stderr.write('pyrockoeost module has been renamed: pyrockoeost.ims\n')
    sys.stderr.write('              -> should now use: pyrockoeost.io.ims\n\n')
    raise ImportError('pyrockoeost module "pyrockoeost.ims" has been renamed to "pyrockoeost.io.ims".')

from pyrockoeost.io.ims import *
