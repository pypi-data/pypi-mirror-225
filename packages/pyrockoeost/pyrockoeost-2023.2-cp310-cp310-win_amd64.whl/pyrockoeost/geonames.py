
import sys
import pyrockoeost
if pyrockoeost.grumpy == 1:
    sys.stderr.write('using renamed pyrockoeost module: pyrockoeost.geonames\n')
    sys.stderr.write('           -> should now use: pyrockoeost.dataset.geonames\n\n')
elif pyrockoeost.grumpy == 2:
    sys.stderr.write('pyrockoeost module has been renamed: pyrockoeost.geonames\n')
    sys.stderr.write('              -> should now use: pyrockoeost.dataset.geonames\n\n')
    raise ImportError('pyrockoeost module "pyrockoeost.geonames" has been renamed to "pyrockoeost.dataset.geonames".')

from pyrockoeost.dataset.geonames import *
