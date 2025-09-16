import numpy as np
import pytest
from task7 import encrypt, decrypt, roundtrip, KEY, INV_KEY

@pytest.mark.parametrize("plain", [
    "",                       # empty
    "Hi!",                    # short
    "The password is: NCS-2014",  # your original example
])
def test_roundtrip_basic(plain):
    assert roundtrip(plain) == plain

def test_encrypt_shape_multiple_of_four():
    # len=5 -> padded to 8 -> 8/4 = 2 columns
    c = encrypt("abcde")
    assert isinstance(c, np.ndarray)
    assert c.shape[0] == 4
    assert c.shape[1] == 2

def test_decrypt_empty_matrix():
    empty = np.empty((4, 0), dtype=int)
    assert decrypt(empty) == ""

def test_specific_key_inverse():
    # sanity: KEY and INV_KEY actually invert the sample
    s = "test 123"
    c = encrypt(s, KEY)
    assert decrypt(c, INV_KEY) == s
