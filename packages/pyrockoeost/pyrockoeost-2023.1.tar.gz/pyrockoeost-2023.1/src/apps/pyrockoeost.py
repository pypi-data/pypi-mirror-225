# http://pyrocko.org - GPLv3
#
# The pyrockoeost Developers, 21st Century
# ---|P------/S----------~Lg----------

import sys
import logging

logger = logging.getLogger('main')


def main():
    logging.basicConfig(
        level=logging.INFO,
        format='pyrockoeost:%(name)-25s - %(levelname)-8s - %(message)s')

    try:
        from pyrockoeost import squirrel

        class PrintVersion(squirrel.SquirrelCommand):
            def make_subparser(self, subparsers):
                return subparsers.add_parser(
                    'version', help='Print version.')

            def setup(self, parser):
                parser.add_argument(
                    '--long',
                    dest='long',
                    action='store_true',
                    help='Print long version string.')

            def run(self, parser, args):
                import pyrockoeost
                if args.long:
                    print(pyrockoeost.long_version)
                else:
                    print(pyrockoeost.__version__)

        class PrintDependencies(squirrel.SquirrelCommand):
            def make_subparser(self, subparsers):
                return subparsers.add_parser(
                    'dependencies',
                    help='Print versions of available dependencies.')

            def setup(self, parser):
                pass

            def run(self, parser, args):
                from pyrockoeost import deps
                deps.print_dependencies()

        class PrintInfo(squirrel.SquirrelCommand):
            def make_subparser(self, subparsers):
                return subparsers.add_parser(
                    'info',
                    help='Print information about pyrockoeost installation(s).')

            def setup(self, parser):
                pass

            def run(self, parser, args):
                from pyrockoeost import deps
                print()
                print('Python executable:\n  %s' % sys.executable)
                print()
                deps.print_installations()

        squirrel.run(
            subcommands=[
                PrintVersion(),
                PrintDependencies(),
                PrintInfo()],
            description='Tools for seismology.')

    except ImportError as e:
        from pyrockoeost import deps
        logger.info('\n' + deps.str_dependencies())
        logger.info('\n' + deps.str_installations())

        try:
            deps.require_all('required')

        except deps.MissingpyrockoeostDependency as e2:
            logger.fatal(str(e2))
            sys.exit(1)

        logger.fatal(str(e))
        sys.exit(1)


if __name__ == '__main__':
    main()
