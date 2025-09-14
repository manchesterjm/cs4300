# src\task6.py

location = "task6_read_me.txt"

# read a file and return the text
def read_file(path):
    # we need to open the file for reading
    with open(path, "r", encoding="utf-8") as f:
        # next we need to read all text into a temp holder var
        text = f.read()
    
    # finally the full text is returned
    return text

# count and return the number of words in the file from a given path
def count_words(path):
    # read all the text from the file path
    latin_text = read_file(path)
    # going to use the whitespace or the " " to determine where words start and end
    words = latin_text.split()
    
    # finally we return the number of words we found
    return len(words)

print(count_words(location))