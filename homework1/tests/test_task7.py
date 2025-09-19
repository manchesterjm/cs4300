#test\test_task7.py

import numpy as np
import pytest
from task7 import encrypt, decrypt, roundtrip, KEY, INV_KEY

@pytest.mark.parametrize("plain", [
    "",                       # empty
    "Hi!",                    # short
    "The password is: NCS-2014",  # original example
])
def test_roundtrip_basic(plain):
    assert roundtrip(plain) == plain

def test_encrypt_shape_multiple_of_four():
    # len=5 -> padded to 8 -> 8/4 = 2 columns
    c = encrypt("abcde")
    # check that it is indeed an numpy array
    assert isinstance(c, np.ndarray)
    # check the "shape" of the array
    assert c.shape[0] == 4
    assert c.shape[1] == 2

def test_decrypt_empty_matrix():
    # what if the matrix is empty?  what happens?
    empty = np.empty((4, 0), dtype=int)
    # check that it is indeed empty
    assert decrypt(empty) == ""

def test_specific_key_inverse():
    # test that the KEY and INV_KEY actually invert the sample
    s = "test 123"
    c = encrypt(s, KEY)
    assert decrypt(c, INV_KEY) == s
