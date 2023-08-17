
import sys
import pyrockoeost
if pyrockoeost.grumpy == 1:
    sys.stderr.write('using renamed pyrockoeost module: pyrockoeost.yaff\n')
    sys.stderr.write('           -> should now use: pyrockoeost.io.yaff\n\n')
elif pyrockoeost.grumpy == 2:
    sys.stderr.write('pyrockoeost module has been renamed: pyrockoeost.yaff\n')
    sys.stderr.write('              -> should now use: pyrockoeost.io.yaff\n\n')
    raise ImportError('pyrockoeost module "pyrockoeost.yaff" has been renamed to "pyrockoeost.io.yaff".')

from pyrockoeost.io.yaff import *
