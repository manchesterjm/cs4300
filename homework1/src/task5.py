favorite_books = [
    # Wheel of Time — Robert Jordan (final 3 with Brandon Sanderson)
    ("The Eye of the World", "Robert Jordan"),
    ("The Great Hunt", "Robert Jordan"),
    ("The Dragon Reborn", "Robert Jordan"),
    ("The Shadow Rising", "Robert Jordan"),
    ("The Fires of Heaven", "Robert Jordan"),
    ("Lord of Chaos", "Robert Jordan"),
    ("A Crown of Swords", "Robert Jordan"),
    ("The Path of Daggers", "Robert Jordan"),
    ("Winters Heart", "Robert Jordan"),
    ("Crossroads of Twilight", "Robert Jordan"),
    ("Knife of Dreams", "Robert Jordan"),
    ("The Gathering Storm", "Robert Jordan & Brandon Sanderson"),
    ("Towers of Midnight", "Robert Jordan & Brandon Sanderson"),
    ("A Memory of Light", "Robert Jordan & Brandon Sanderson"),

    # Dune (original six) — Frank Herbert
    ("Dune", "Frank Herbert"),
    ("Dune Messiah", "Frank Herbert"),
    ("Children of Dune", "Frank Herbert"),
    ("God Emperor of Dune", "Frank Herbert"),
    ("Heretics of Dune", "Frank Herbert"),
    ("Chapterhouse: Dune", "Frank Herbert"),

    # Harry Potter — J. K. Rowling
    ("Harry Potter and the Sorcerers Stone", "J. K. Rowling"),
    ("Harry Potter and the Chamber of Secrets", "J. K. Rowling"),
    ("Harry Potter and the Prisoner of Azkaban", "J. K. Rowling"),
    ("Harry Potter and the Goblet of Fire", "J. K. Rowling"),
    ("Harry Potter and the Order of the Phoenix", "J. K. Rowling"),
    ("Harry Potter and the Half-Blood Prince", "J. K. Rowling"),
    ("Harry Potter and the Deathly Hallows", "J. K. Rowling"),
]

# student database using student number as the key and the student last name as the value
student_database = {
    "00001": "Thompson",
    "00002": "Scott",
    "00003": "Carter",
    "00004": "Mitchell",
    "00005": "Hughes",
    "00006": "Ramirez",
    "00007": "Wilson",
    "00008": "Murphy",
    "00009": "Collins",
    "00010": "Hayes",
    "00011": "Cooper",
    "00012": "Foster",
    "00013": "Parker",
    "00014": "Turner",
    "00015": "Bennett",
    "00016": "Ward",
    "00017": "Reed",
    "00018": "Price",
    "00019": "Barnes",
    "00020": "Brooks",
}

def print_book(book_list):
    return book_list[:3]

# print(print_book(favorite_books))