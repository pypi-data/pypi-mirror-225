
import sys
import pyrockoeost
if pyrockoeost.grumpy == 1:
    sys.stderr.write('using renamed pyrockoeost module: pyrockoeost.snuffler\n')
    sys.stderr.write('           -> should now use: pyrockoeost.gui.snuffler.snuffler\n\n')
elif pyrockoeost.grumpy == 2:
    sys.stderr.write('pyrockoeost module has been renamed: pyrockoeost.snuffler\n')
    sys.stderr.write('              -> should now use: pyrockoeost.gui.snuffler.snuffler\n\n')
    raise ImportError('pyrockoeost module "pyrockoeost.snuffler" has been renamed to "pyrockoeost.gui.snuffler.snuffler".')

from pyrockoeost.gui.snuffler.snuffler import *
