from fp2md4roam.author import Author
from fp2md4roam.filing import RoamFileMaker
from logzero import logger, loglevel, WARN

from fp2md4roam.visitor import RawMap


def read(name: str):
    with open(name) as inp:
        result = inp.read()
    return result


def convert(path, filer: RoamFileMaker):
    loglevel(WARN)
    logger.info('converting %s %s' % (path, filer.target_directory()))
    map = RawMap(read(path), path)
    Author(filer).visit(map)