# tests/test_task6.py

from task6 import read_file, count_words

path = "task6_read_me.txt"

def test_read_file_returns_text():
    # read the latin test file and make sure we get some text back
    text = read_file(path)
    # check that it is text
    assert isinstance(text, str)
    # check that it is not a blank document
    assert len(text) > 0

def test_count_words_readme():
    # and now we count the words
    assert count_words(path) == 125