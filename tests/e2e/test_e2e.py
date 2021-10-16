import os
import shutil
from unittest import TestCase
from hamcrest import assert_that, contains_string, is_not
from fp2md4roam.convert import convert
from os.path import join, exists, isfile

# As an end-to-end test, this needs to muck about with the file system.:(
from fp2md4roam.filing import FSFiler, RoamFileMaker

DATA_DIRECTORY = 'tests/test-data'
TEST_DIRECTORY = join(DATA_DIRECTORY,'generated')
MARKDOWN_FILE_DIRECTORY =  join(TEST_DIRECTORY, 'markdown')
IMAGES = join(MARKDOWN_FILE_DIRECTORY, 'images')


def prepare_test_directories():
    if os.path.exists(TEST_DIRECTORY):  # pragma: no cover
        shutil.rmtree(TEST_DIRECTORY)


def contents_of_manuscript(file_name):
    path = join(MARKDOWN_FILE_DIRECTORY, file_name)
    with open(path) as file_to_read:
        return file_to_read.read()


def check_file_contains(chapter, *texts):
    md = contents_of_manuscript(chapter)
    for text in texts:
        assert_that(md, contains_string(text))


def check_file_excludes(chapter, *texts):
    md = contents_of_manuscript(chapter)
    for text in texts:
        assert_that(md, is_not(contains_string(text)))


def check_image(image_name):
    full_image_path = os.path.join(IMAGES, image_name)
    assert_that(exists(full_image_path) and isfile(full_image_path), 'file <%s> expected but does not exist' % image_name)


class ConverterTest(TestCase):
    def setUp(self) -> None:
        prepare_test_directories()

    def test_handles_real_map(self):
        test_map = 'BrainRules.mm'
        self.convert_test_map(test_map)
        check_file_contains('BrainRules.md', '# Brain Rules')

    @staticmethod
    def convert_test_map(test_map):
        source = join(DATA_DIRECTORY, 'source')
        fs_filer = RoamFileMaker(FSFiler(TEST_DIRECTORY))
        convert(os.path.join(source, test_map), fs_filer)


