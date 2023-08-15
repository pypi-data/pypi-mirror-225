
import sys
import pyrockoeost
if pyrockoeost.grumpy == 1:
    sys.stderr.write('using renamed pyrockoeost module: pyrockoeost.fdsn.ws\n')
    sys.stderr.write('           -> should now use: pyrockoeost.client.fdsn\n\n')
elif pyrockoeost.grumpy == 2:
    sys.stderr.write('pyrockoeost module has been renamed: pyrockoeost.fdsn.ws\n')
    sys.stderr.write('              -> should now use: pyrockoeost.client.fdsn\n\n')
    raise ImportError('pyrockoeost module "pyrockoeost.fdsn.ws" has been renamed to "pyrockoeost.client.fdsn".')

from pyrockoeost.client.fdsn import *
