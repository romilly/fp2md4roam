import os
import shutil
from unittest import TestCase
from hamcrest import assert_that, contains_string, is_not
from fp2md4roam.convert import convert
from os.path import join, exists, isfile


DATA_DIRECTORY = 'tests/test-data'
TEST_DIRECTORY = join(DATA_DIRECTORY,'generated')


def prepare_test_directories():
    if os.path.exists(TEST_DIRECTORY):  # pragma: no cover
        shutil.rmtree(TEST_DIRECTORY)


def contents_of_manuscript(file_name):
    path = join(TEST_DIRECTORY, file_name)
    if not os.path.exists(path):
        raise ValueError('file %s does not exist' % path)
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


class ConverterTest(TestCase):
    def setUp(self) -> None:
        prepare_test_directories()

    def test_handles_minimal_map(self):
        test_map = 'TestMap.mm'
        self.convert_test_map(test_map)
        check_file_excludes('TestMap.md', '-')

    def test_handles_map_with_punctuation_in_root(self):
        test_map = 'TestMap2.mm'
        self.convert_test_map(test_map)
        check_file_excludes('TestMapwithnewlinesandpunctuation.md', '-')

    def test_handles_map_with_branches(self):
        test_map = 'TestMap1.mm'
        self.convert_test_map(test_map)
        check_file_contains('TestMapOne.md',
                            '- First branch',
                            '- Second Branch',
                            '\t\t- branch 2.1',
                            '\t\t- [branch with link](https://www.bbc.co.uk/news)',
                            '- _Third_ branch',
                            '- Fourth branch\nHas in-line description'
                            )


    @staticmethod
    def convert_test_map(test_map):
        source = join(DATA_DIRECTORY, 'source', test_map)
        convert(source, TEST_DIRECTORY)


