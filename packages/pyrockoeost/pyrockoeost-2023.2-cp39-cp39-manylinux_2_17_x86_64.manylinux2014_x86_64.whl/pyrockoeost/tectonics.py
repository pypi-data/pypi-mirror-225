
import sys
import pyrockoeost
if pyrockoeost.grumpy == 1:
    sys.stderr.write('using renamed pyrockoeost module: pyrockoeost.tectonics\n')
    sys.stderr.write('           -> should now use: pyrockoeost.dataset.tectonics\n\n')
elif pyrockoeost.grumpy == 2:
    sys.stderr.write('pyrockoeost module has been renamed: pyrockoeost.tectonics\n')
    sys.stderr.write('              -> should now use: pyrockoeost.dataset.tectonics\n\n')
    raise ImportError('pyrockoeost module "pyrockoeost.tectonics" has been renamed to "pyrockoeost.dataset.tectonics".')

from pyrockoeost.dataset.tectonics import *
