
import sys
import pyrockoeost
if pyrockoeost.grumpy == 1:
    sys.stderr.write('using renamed pyrockoeost module: pyrockoeost.pile_viewer\n')
    sys.stderr.write('           -> should now use: pyrockoeost.gui.snuffler.pile_viewer\n\n')
elif pyrockoeost.grumpy == 2:
    sys.stderr.write('pyrockoeost module has been renamed: pyrockoeost.pile_viewer\n')
    sys.stderr.write('              -> should now use: pyrockoeost.gui.snuffler.pile_viewer\n\n')
    raise ImportError('pyrockoeost module "pyrockoeost.pile_viewer" has been renamed to "pyrockoeost.gui.snuffler.pile_viewer".')

from pyrockoeost.gui.snuffler.pile_viewer import *
