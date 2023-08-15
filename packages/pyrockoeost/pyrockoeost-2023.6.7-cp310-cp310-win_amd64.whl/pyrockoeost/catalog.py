
import sys
import pyrockoeost
if pyrockoeost.grumpy == 1:
    sys.stderr.write('using renamed pyrockoeost module: pyrockoeost.catalog\n')
    sys.stderr.write('           -> should now use: pyrockoeost.client.catalog\n\n')
elif pyrockoeost.grumpy == 2:
    sys.stderr.write('pyrockoeost module has been renamed: pyrockoeost.catalog\n')
    sys.stderr.write('              -> should now use: pyrockoeost.client.catalog\n\n')
    raise ImportError('pyrockoeost module "pyrockoeost.catalog" has been renamed to "pyrockoeost.client.catalog".')

from pyrockoeost.client.catalog import *
