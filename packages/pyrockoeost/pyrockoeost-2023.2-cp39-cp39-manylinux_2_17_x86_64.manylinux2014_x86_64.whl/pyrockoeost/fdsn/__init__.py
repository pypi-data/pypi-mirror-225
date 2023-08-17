
import sys
import pyrockoeost
if pyrockoeost.grumpy == 1:
    sys.stderr.write('using renamed pyrockoeost module: pyrockoeost.fdsn.__init__\n')
    sys.stderr.write('           -> should now use: \n\n')
elif pyrockoeost.grumpy == 2:
    sys.stderr.write('pyrockoeost module has been renamed: pyrockoeost.fdsn.__init__\n')
    sys.stderr.write('              -> should now use: \n\n')
    raise ImportError('pyrockoeost module "pyrockoeost.fdsn.__init__" has been renamed to "".')

