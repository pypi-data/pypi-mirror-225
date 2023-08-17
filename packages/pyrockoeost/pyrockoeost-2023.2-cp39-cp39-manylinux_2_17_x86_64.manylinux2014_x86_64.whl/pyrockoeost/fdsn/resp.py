
import sys
import pyrockoeost
if pyrockoeost.grumpy == 1:
    sys.stderr.write('using renamed pyrockoeost module: pyrockoeost.fdsn.resp\n')
    sys.stderr.write('           -> should now use: pyrockoeost.io.resp\n\n')
elif pyrockoeost.grumpy == 2:
    sys.stderr.write('pyrockoeost module has been renamed: pyrockoeost.fdsn.resp\n')
    sys.stderr.write('              -> should now use: pyrockoeost.io.resp\n\n')
    raise ImportError('pyrockoeost module "pyrockoeost.fdsn.resp" has been renamed to "pyrockoeost.io.resp".')

from pyrockoeost.io.resp import *
