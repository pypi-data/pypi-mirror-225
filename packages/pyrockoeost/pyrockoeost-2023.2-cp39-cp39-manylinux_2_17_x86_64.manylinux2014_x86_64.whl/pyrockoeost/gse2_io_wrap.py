
import sys
import pyrockoeost
if pyrockoeost.grumpy == 1:
    sys.stderr.write('using renamed pyrockoeost module: pyrockoeost.gse2_io_wrap\n')
    sys.stderr.write('           -> should now use: pyrockoeost.io.gse2\n\n')
elif pyrockoeost.grumpy == 2:
    sys.stderr.write('pyrockoeost module has been renamed: pyrockoeost.gse2_io_wrap\n')
    sys.stderr.write('              -> should now use: pyrockoeost.io.gse2\n\n')
    raise ImportError('pyrockoeost module "pyrockoeost.gse2_io_wrap" has been renamed to "pyrockoeost.io.gse2".')

from pyrockoeost.io.gse2 import *
