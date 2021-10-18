import sys
from fp2md4roam.convert import convert


def converter(): # pragma: no cover
    if len(sys.argv) != 3:
        print('usage: python3 convert.py path_to_map target_directory')
        sys.exit(1)
    map_path = sys.argv[1]
    target_dir = sys.argv[2]
    convert(map_path, target_dir)


if __name__ == '__main__': # pragma: no cover
    converter()

