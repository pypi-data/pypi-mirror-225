
import sys
import pyrockoeost
if pyrockoeost.grumpy == 1:
    sys.stderr.write('using renamed pyrockoeost module: pyrockoeost.seisan_waveform\n')
    sys.stderr.write('           -> should now use: pyrockoeost.io.seisan_waveform\n\n')
elif pyrockoeost.grumpy == 2:
    sys.stderr.write('pyrockoeost module has been renamed: pyrockoeost.seisan_waveform\n')
    sys.stderr.write('              -> should now use: pyrockoeost.io.seisan_waveform\n\n')
    raise ImportError('pyrockoeost module "pyrockoeost.seisan_waveform" has been renamed to "pyrockoeost.io.seisan_waveform".')

from pyrockoeost.io.seisan_waveform import *
