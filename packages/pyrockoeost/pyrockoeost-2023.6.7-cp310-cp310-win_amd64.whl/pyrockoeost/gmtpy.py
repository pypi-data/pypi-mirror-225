
import sys
import pyrockoeost
if pyrockoeost.grumpy == 1:
    sys.stderr.write('using renamed pyrockoeost module: pyrockoeost.gmtpy\n')
    sys.stderr.write('           -> should now use: pyrockoeost.plot.gmtpy\n\n')
elif pyrockoeost.grumpy == 2:
    sys.stderr.write('pyrockoeost module has been renamed: pyrockoeost.gmtpy\n')
    sys.stderr.write('              -> should now use: pyrockoeost.plot.gmtpy\n\n')
    raise ImportError('pyrockoeost module "pyrockoeost.gmtpy" has been renamed to "pyrockoeost.plot.gmtpy".')

from pyrockoeost.plot.gmtpy import *
