
import sys
import pyrockoeost
if pyrockoeost.grumpy == 1:
    sys.stderr.write('using renamed pyrockoeost module: pyrockoeost.topo\n')
    sys.stderr.write('           -> should now use: pyrockoeost.dataset.topo\n\n')
elif pyrockoeost.grumpy == 2:
    sys.stderr.write('pyrockoeost module has been renamed: pyrockoeost.topo\n')
    sys.stderr.write('              -> should now use: pyrockoeost.dataset.topo\n\n')
    raise ImportError('pyrockoeost module "pyrockoeost.topo" has been renamed to "pyrockoeost.dataset.topo".')

from pyrockoeost.dataset.topo import *
