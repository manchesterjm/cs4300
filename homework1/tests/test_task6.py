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

''' def test_count_words_cases_loop(tmp_path):
    # create cases that we can throw at my functions for testing
    cases = [
        ("", 0),
        (" ", 0),
        ("one two", 2),
        ("one\ntwo\tthree", 3),
        ("one\ntwo three four ", 4),
    ] '''

@pytest.mark.parametrize("text, expected", [
    ("", 0),
    (" ", 0),
    ("one two", 2),
    ("one\ntwo\tthree", 3),
    ("one\ntwo three four ", 4),
])

    # create a temp file from the cases for testing count_words and read_file
    for text, expected in cases:
        p = tmp_path / "t.txt"
        p.write_text(text, encoding="utf-8") # I found I needed to specify encoding since I specifiy reading it as such

        # test that the function returns the expected number of words
        assert count_words(str(p)) == expected