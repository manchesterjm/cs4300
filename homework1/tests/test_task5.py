from task5 import print_book, favorite_books, student_database

##################################### tests for book list #########################################
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

def test_len_first_three():
    # we needed to print out the first three books
    # test that the length of the list returned is 3
    assert len(print_book(favorite_books)) == 3

def test_print_book_func():
    # make sure that the first three books that the print function prints is indeed the frist three books listed
    assert print_book(favorite_books) == favorite_books[:3]

################################# tests for student database #######################################

student_ids = list(student_database.keys())
l_names = list(student_database.values())
db_length = len(student_database)

def test_lengths_ids_lnames():
    # find the length of the database and test that we have the same number of
    # ids and names
    assert db_length == len(l_names) == len(student_ids)

def test_database_is_dict():
    # the database needs to be a dictionary
    # test if database is dict
    assert isinstance(student_database, dict)

def test_student_last_names():
    # test that each student name is not an empty string, i.e. something exists
    for l_name in l_names:
        assert isinstance(l_name, str)

def test_student_ids():
    # we made each student ID 5 digits long
    # test that each student ID is exactly 5 digits
    for id in student_ids:
        assert len(id) == 5