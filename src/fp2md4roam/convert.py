import sys

from fp2md4roam.author import Author, RawMap
from fp2md4roam.filing import FSFiler
from logzero import logger, loglevel, WARN


def read(name: str):
    with open(name) as inp:
        result = inp.read()
    return result


def convert(path, target_directory):
    loglevel(WARN)
    filer = FSFiler(target_directory)
    logger.info('converting %s %s' % (path, filer.target_directory))
    mindmap = RawMap(read(path), path)
    Author(filer).visit(mindmap)


