
import sys
import pyrockoeost
if pyrockoeost.grumpy == 1:
    sys.stderr.write('using renamed pyrockoeost module: pyrockoeost.iris_ws\n')
    sys.stderr.write('           -> should now use: pyrockoeost.client.iris\n\n')
elif pyrockoeost.grumpy == 2:
    sys.stderr.write('pyrockoeost module has been renamed: pyrockoeost.iris_ws\n')
    sys.stderr.write('              -> should now use: pyrockoeost.client.iris\n\n')
    raise ImportError('pyrockoeost module "pyrockoeost.iris_ws" has been renamed to "pyrockoeost.client.iris".')

from pyrockoeost.client.iris import *
