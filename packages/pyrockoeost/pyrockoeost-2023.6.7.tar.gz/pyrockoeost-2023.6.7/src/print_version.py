# https://pyrocko.org - GPLv3
#
# The pyrockoeost Developers, 21st Century
# ---|P------/S----------~Lg----------

import sys


def print_version(deps=False):
    import pyrockoeost
    if deps:
        print('pyrockoeost: %s' % pyrockoeost.long_version)
        try:
            import numpy
            print('numpy: %s' % numpy.__version__)
        except ImportError:
            print('numpy: N/A')

        try:
            import scipy
            print('scipy: %s' % scipy.__version__)
        except ImportError:
            print('scipy: N/A')

        try:
            import matplotlib
            print('matplotlib: %s' % matplotlib.__version__)
        except ImportError:
            print('matplotlib: N/A')

        try:
            from pyrockoeost.gui.qt_compat import Qt
            print('PyQt: %s' % Qt.PYQT_VERSION_STR)
            print('Qt: %s' % Qt.QT_VERSION_STR)
        except ImportError:
            print('PyQt: N/A')
            print('Qt: N/A')

        try:
            import vtk
            print('VTK: %s' % vtk.VTK_VERSION)
        except ImportError:
            print('VTK: N/A')

        print('python: %s.%s.%s' % sys.version_info[:3])

    elif sys.argv[1:] == ['short']:
        print(pyrockoeost.version)
    else:
        print(pyrockoeost.long_version)


if __name__ == '__main__':
    print_version(sys.argv[1:] == ['deps'])
