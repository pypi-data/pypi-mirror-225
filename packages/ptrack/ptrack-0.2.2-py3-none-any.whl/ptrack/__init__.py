import argparse
version="0.2.2"

parser = argparse.ArgumentParser(description='A simple CLI utility for asthetically tracking progress when copying or moving files.')
parser.add_argument('-v', '--verbose', action='store_true', help='verbose output')
parser.add_argument('-c', '--copy', action='store_true', help='copy files (You can use `ptc` instead of `ptrack -c`)')
parser.add_argument('-m', '--move', action='store_true', help='move files (You can use `ptm` instead of `ptrack -m`)')
parser.add_argument('-d', '--download', action='store_true', help='download files (You can use `ptd` instead of `ptrack -d`)')
parser.add_argument('-V', '--version', action='version', version='%(prog)s' + version)

args, unknown = parser.parse_known_args()

verbose = args.verbose
copy = args.copy
move = args.move
download = args.download
