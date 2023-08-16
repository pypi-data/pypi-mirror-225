import argparse
from hides import __title__, __version__


def main() -> None:

    parser = argparse.ArgumentParser(description='Run HIDES')
    parser.add_argument('-f', '--file', type=str,
                        help="input file location", nargs="?")
    parser.add_argument('-i', '--inspect', type=str,
                        help="Scan/inspect file for virus or vulnerability", metavar='')
    parser.add_argument('-v', '--version', help="Version", action="store_true")

    args = parser.parse_args()

    if args.version:
        print(f"{__title__} version {__version__}")
        return
    
    print(f"-f {args.file}")


if __name__ == '__main__':
    main()
