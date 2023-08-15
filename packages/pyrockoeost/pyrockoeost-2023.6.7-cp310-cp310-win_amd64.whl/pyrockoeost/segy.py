
import sys
import pyrockoeost
if pyrockoeost.grumpy == 1:
    sys.stderr.write('using renamed pyrockoeost module: pyrockoeost.segy\n')
    sys.stderr.write('           -> should now use: pyrockoeost.io.segy\n\n')
elif pyrockoeost.grumpy == 2:
    sys.stderr.write('pyrockoeost module has been renamed: pyrockoeost.segy\n')
    sys.stderr.write('              -> should now use: pyrockoeost.io.segy\n\n')
    raise ImportError('pyrockoeost module "pyrockoeost.segy" has been renamed to "pyrockoeost.io.segy".')

from pyrockoeost.io.segy import *
