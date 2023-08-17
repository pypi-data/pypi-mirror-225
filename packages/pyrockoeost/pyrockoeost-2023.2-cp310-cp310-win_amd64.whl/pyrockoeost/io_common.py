
import sys
import pyrockoeost
if pyrockoeost.grumpy == 1:
    sys.stderr.write('using renamed pyrockoeost module: pyrockoeost.io_common\n')
    sys.stderr.write('           -> should now use: pyrockoeost.io.io_common\n\n')
elif pyrockoeost.grumpy == 2:
    sys.stderr.write('pyrockoeost module has been renamed: pyrockoeost.io_common\n')
    sys.stderr.write('              -> should now use: pyrockoeost.io.io_common\n\n')
    raise ImportError('pyrockoeost module "pyrockoeost.io_common" has been renamed to "pyrockoeost.io.io_common".')

from pyrockoeost.io.io_common import *
