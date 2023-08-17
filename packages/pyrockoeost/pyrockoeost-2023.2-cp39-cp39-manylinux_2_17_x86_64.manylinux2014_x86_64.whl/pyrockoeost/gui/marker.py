
import sys
import pyrockoeost
if pyrockoeost.grumpy == 1:
    sys.stderr.write('using renamed pyrockoeost module: pyrockoeost.gui.marker\n')
    sys.stderr.write('           -> should now use: pyrockoeost.gui.snuffler.marker\n\n')
elif pyrockoeost.grumpy == 2:
    sys.stderr.write('pyrockoeost module has been renamed: pyrockoeost.gui.marker\n')
    sys.stderr.write('              -> should now use: pyrockoeost.gui.snuffler.marker\n\n')
    raise ImportError('pyrockoeost module "pyrockoeost.gui.marker" has been renamed to "pyrockoeost.gui.snuffler.marker".')

from pyrockoeost.gui.snuffler.marker import *
