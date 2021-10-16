from fp2md4roam.author import Author, RawMap
from fp2md4roam.filing import RoamFileMaker
from logzero import logger, loglevel, WARN


def read(name: str):
    with open(name) as inp:
        result = inp.read()
    return result


def convert(path, filer: RoamFileMaker):
    loglevel(WARN)
    logger.info('converting %s %s' % (path, filer.target_directory()))
    map = RawMap(read(path), path)
    Author(filer).visit(map)