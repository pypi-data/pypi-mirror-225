
import sys
import pyrockoeost
if pyrockoeost.grumpy == 1:
    sys.stderr.write('using renamed pyrockoeost module: pyrockoeost.gse1\n')
    sys.stderr.write('           -> should now use: pyrockoeost.io.gse1\n\n')
elif pyrockoeost.grumpy == 2:
    sys.stderr.write('pyrockoeost module has been renamed: pyrockoeost.gse1\n')
    sys.stderr.write('              -> should now use: pyrockoeost.io.gse1\n\n')
    raise ImportError('pyrockoeost module "pyrockoeost.gse1" has been renamed to "pyrockoeost.io.gse1".')

from pyrockoeost.io.gse1 import *
