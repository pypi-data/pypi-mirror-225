# http://pyrocko.org - GPLv3
#
# The pyrockoeost Developers, 21st Century
# ---|P------/S----------~Lg----------

class SquirrelError(Exception):
    pass


class NotAvailable(SquirrelError):
    pass


class Duplicate(SquirrelError):
    pass


class Inconsistencies(SquirrelError):
    pass


class ConversionError(SquirrelError):
    pass


class ToolError(Exception):
    pass


__all__ = [
    'SquirrelError',
    'ToolError',
    'NotAvailable']
