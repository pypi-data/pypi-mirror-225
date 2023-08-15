# https://pyrocko.org - GPLv3
#
# The pyrockoeost Developers, 21st Century
# ---|P------/S----------~Lg----------

from pyrockoeost.gui.snuffler import snuffler


def main(args=None):
    snuffler.snuffler_from_commandline(args=args)


if __name__ == '__main__':
    main()
