
import sys
import pyrockoeost
if pyrockoeost.grumpy == 1:
    sys.stderr.write('using renamed pyrockoeost module: pyrockoeost.crustdb\n')
    sys.stderr.write('           -> should now use: pyrockoeost.dataset.crustdb\n\n')
elif pyrockoeost.grumpy == 2:
    sys.stderr.write('pyrockoeost module has been renamed: pyrockoeost.crustdb\n')
    sys.stderr.write('              -> should now use: pyrockoeost.dataset.crustdb\n\n')
    raise ImportError('pyrockoeost module "pyrockoeost.crustdb" has been renamed to "pyrockoeost.dataset.crustdb".')

from pyrockoeost.dataset.crustdb import *
