
import sys
import pyrockoeost
if pyrockoeost.grumpy == 1:
    sys.stderr.write('using renamed pyrockoeost module: pyrockoeost.suds\n')
    sys.stderr.write('           -> should now use: pyrockoeost.io.suds\n\n')
elif pyrockoeost.grumpy == 2:
    sys.stderr.write('pyrockoeost module has been renamed: pyrockoeost.suds\n')
    sys.stderr.write('              -> should now use: pyrockoeost.io.suds\n\n')
    raise ImportError('pyrockoeost module "pyrockoeost.suds" has been renamed to "pyrockoeost.io.suds".')

from pyrockoeost.io.suds import *
