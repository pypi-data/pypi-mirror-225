# http://pyrocko.org - GPLv3
#
# The pyrockoeost Developers, 21st Century
# ---|P------/S----------~Lg----------

class ScenarioError(Exception):
    pass


class LocationGenerationError(ScenarioError):
    pass


class CannotCreatePath(ScenarioError):
    pass


__all__ = ['ScenarioError', 'LocationGenerationError', 'CannotCreatePath']
