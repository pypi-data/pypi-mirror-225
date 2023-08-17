
import sys
import pyrockoeost
if pyrockoeost.grumpy == 1:
    sys.stderr.write('using renamed pyrockoeost module: pyrockoeost.crust2x2\n')
    sys.stderr.write('           -> should now use: pyrockoeost.dataset.crust2x2\n\n')
elif pyrockoeost.grumpy == 2:
    sys.stderr.write('pyrockoeost module has been renamed: pyrockoeost.crust2x2\n')
    sys.stderr.write('              -> should now use: pyrockoeost.dataset.crust2x2\n\n')
    raise ImportError('pyrockoeost module "pyrockoeost.crust2x2" has been renamed to "pyrockoeost.dataset.crust2x2".')

from pyrockoeost.dataset.crust2x2 import *
