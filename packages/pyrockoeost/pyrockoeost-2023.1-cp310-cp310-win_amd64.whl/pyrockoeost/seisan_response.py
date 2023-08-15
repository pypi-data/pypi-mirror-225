
import sys
import pyrockoeost
if pyrockoeost.grumpy == 1:
    sys.stderr.write('using renamed pyrockoeost module: pyrockoeost.seisan_response\n')
    sys.stderr.write('           -> should now use: pyrockoeost.io.seisan_response\n\n')
elif pyrockoeost.grumpy == 2:
    sys.stderr.write('pyrockoeost module has been renamed: pyrockoeost.seisan_response\n')
    sys.stderr.write('              -> should now use: pyrockoeost.io.seisan_response\n\n')
    raise ImportError('pyrockoeost module "pyrockoeost.seisan_response" has been renamed to "pyrockoeost.io.seisan_response".')

from pyrockoeost.io.seisan_response import *
