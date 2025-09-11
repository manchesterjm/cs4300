from task5 import print_book, favorite_books, student_database

def test_book_list_valid():
    # test that the book list is in fact a list as the assignment calls for
    assert isinstance(favorite_books, list)

def test_length_book_list():
    # since I need to print out the first three books we can assume we needed a list > 3 books
    # test that the list is > 3
    assert len(favorite_books) > 3

def test_title_auther_exist():
    # the assignment stated that we needed the book title and authoer
    # test that each book in the list has a title and an author assigned
    for title, author in favorite_books:
        assert isinstance(title, str) # not looking for a correct name, just that one exists
        assert isinstance(author, str) # does an author exist
 
def test_print_book_func():
    # make sure that the first three books that the print function prints is indeed the frist three books listed
    assert print_book(favorite_books) == favorite_books[:3]