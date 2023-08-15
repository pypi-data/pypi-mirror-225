
import sys
import pyrockoeost
if pyrockoeost.grumpy == 1:
    sys.stderr.write('using renamed pyrockoeost module: pyrockoeost.gui_util\n')
    sys.stderr.write('           -> should now use: pyrockoeost.gui.util\n\n')
elif pyrockoeost.grumpy == 2:
    sys.stderr.write('pyrockoeost module has been renamed: pyrockoeost.gui_util\n')
    sys.stderr.write('              -> should now use: pyrockoeost.gui.util\n\n')
    raise ImportError('pyrockoeost module "pyrockoeost.gui_util" has been renamed to "pyrockoeost.gui.util".')

from pyrockoeost.gui.util import *
