import sys

from fp2md4roam.author import Author, RawMap
from fp2md4roam.filing import RoamFileMaker, FSFiler
from logzero import logger, loglevel, WARN


def read(name: str):
    with open(name) as inp:
        result = inp.read()
    return result


def convert(path, target_directory):
    loglevel(WARN)
    filer = RoamFileMaker(FSFiler(target_directory))
    logger.info('converting %s %s' % (path, filer.target_directory()))
    mindmap = RawMap(read(path), path)
    Author(filer).visit(mindmap)


def converter():
    if len(sys.argv) != 3:
        print('usage: python3 convert.py path_to_map target_directory')
        sys.exit(1)
    map_path = sys.argv[1]
    target_dir = sys.argv[2]
    convert(map_path, target_dir)


