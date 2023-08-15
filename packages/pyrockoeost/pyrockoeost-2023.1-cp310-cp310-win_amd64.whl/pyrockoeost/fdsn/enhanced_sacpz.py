
import sys
import pyrockoeost
if pyrockoeost.grumpy == 1:
    sys.stderr.write('using renamed pyrockoeost module: pyrockoeost.fdsn.enhanced_sacpz\n')
    sys.stderr.write('           -> should now use: pyrockoeost.io.enhanced_sacpz\n\n')
elif pyrockoeost.grumpy == 2:
    sys.stderr.write('pyrockoeost module has been renamed: pyrockoeost.fdsn.enhanced_sacpz\n')
    sys.stderr.write('              -> should now use: pyrockoeost.io.enhanced_sacpz\n\n')
    raise ImportError('pyrockoeost module "pyrockoeost.fdsn.enhanced_sacpz" has been renamed to "pyrockoeost.io.enhanced_sacpz".')

from pyrockoeost.io.enhanced_sacpz import *
