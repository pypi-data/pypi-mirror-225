# http://pyrocko.org - GPLv3
#
# The pyrockoeost Developers, 21st Century
# ---|P------/S----------~Lg----------

from pyrockoeost import gf
from .error import CannotCreatePath


def remake_dir(dpath, force):
    try:
        return gf.store.remake_dir(dpath, force)

    except gf.CannotCreate as e:
        raise CannotCreatePath(str(e))
