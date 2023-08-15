
import sys
import pyrockoeost
if pyrockoeost.grumpy == 1:
    sys.stderr.write('using renamed pyrockoeost module: pyrockoeost.eventdata\n')
    sys.stderr.write('           -> should now use: pyrockoeost.io.eventdata\n\n')
elif pyrockoeost.grumpy == 2:
    sys.stderr.write('pyrockoeost module has been renamed: pyrockoeost.eventdata\n')
    sys.stderr.write('              -> should now use: pyrockoeost.io.eventdata\n\n')
    raise ImportError('pyrockoeost module "pyrockoeost.eventdata" has been renamed to "pyrockoeost.io.eventdata".')

from pyrockoeost.io.eventdata import *
