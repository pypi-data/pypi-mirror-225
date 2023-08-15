
import sys
import pyrockoeost
if pyrockoeost.grumpy == 1:
    sys.stderr.write('using renamed pyrockoeost module: pyrockoeost.css\n')
    sys.stderr.write('           -> should now use: pyrockoeost.io.css\n\n')
elif pyrockoeost.grumpy == 2:
    sys.stderr.write('pyrockoeost module has been renamed: pyrockoeost.css\n')
    sys.stderr.write('              -> should now use: pyrockoeost.io.css\n\n')
    raise ImportError('pyrockoeost module "pyrockoeost.css" has been renamed to "pyrockoeost.io.css".')

from pyrockoeost.io.css import *
