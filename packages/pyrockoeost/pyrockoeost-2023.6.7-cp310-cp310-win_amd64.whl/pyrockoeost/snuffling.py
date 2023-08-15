
import sys
import pyrockoeost
if pyrockoeost.grumpy == 1:
    sys.stderr.write('using renamed pyrockoeost module: pyrockoeost.snuffling\n')
    sys.stderr.write('           -> should now use: pyrockoeost.gui.snuffler.snuffling\n\n')
elif pyrockoeost.grumpy == 2:
    sys.stderr.write('pyrockoeost module has been renamed: pyrockoeost.snuffling\n')
    sys.stderr.write('              -> should now use: pyrockoeost.gui.snuffler.snuffling\n\n')
    raise ImportError('pyrockoeost module "pyrockoeost.snuffling" has been renamed to "pyrockoeost.gui.snuffler.snuffling".')

from pyrockoeost.gui.snuffler.snuffling import *
