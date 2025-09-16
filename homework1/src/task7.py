# src\task7.py

import numpy as np

# 4x4 key matrices (integers). inv_key reverses key exactly.
KEY = np.array(
    [
        [1, -1, -1,  1],
        [2, -3, -5,  4],
        [-2, -1, -2, 2],
        [3, -3, -1,  2],
    ],
    dtype=int,
)

INV_KEY = np.array(
    [
        [ 6, -1, 0, -1],
        [22, -4, 1, -4],
        [14, -3, 1, -2],
        [31, -6, 2, -5],
    ],
    dtype=int,
)


# convert text -> 4xn int matrix (column-major, padded with 0)
def _text_to_blocks(text: str) -> np.ndarray:
    # make unicode code points for each character
    codes = [ord(ch) for ch in text]

    # pad the list so its length is a multiple of 4
    while len(codes) % 4 != 0:
        codes.append(0)

    # special case: empty input -> empty (4x0) matrix
    if len(codes) == 0:
        return np.empty((4, 0), dtype=int)

    # shape as 4 x n by filling rows then transposing to columns
    arr = np.array(codes, dtype=int).reshape(-1, 4).T  # 4 x n
    return arr


# convert 4xn int matrix -> text (strip trailing padding zeros)
def _blocks_to_text(blocks: np.ndarray) -> str:
    if blocks.size == 0:
        return ""

    # bring back to flat sequence in original order
    flat = blocks.T.reshape(-1).tolist()

    # drop only trailing zeros from padding
    while flat and flat[-1] == 0:
        flat.pop()

    # turn code points back into characters
    return "".join(chr(v) for v in flat)


# encrypt plain text to integer matrix using KEY
def encrypt(text: str, key: np.ndarray = KEY) -> np.ndarray:
    blocks = _text_to_blocks(text)       # 4 x n
    # matrix multiply (NumPy shows off here)
    cipher = key @ blocks                # 4 x n
    return cipher


# decrypt integer matrix back to plain text using INV_KEY
def decrypt(cipher: np.ndarray, inv_key: np.ndarray = INV_KEY) -> str:
    if cipher.size == 0:
        return ""
    # multiply by inverse
    blocks = inv_key @ cipher            # 4 x n
    # convert back to text
    return _blocks_to_text(blocks)


# quick round-trip helper
def roundtrip(text: str) -> str:
    return decrypt(encrypt(text))


if __name__ == "__main__":
    # small demo
    demo = "The password is: NCS-2014"
    c = encrypt(demo)
    p = decrypt(c)
    print(p)  # should print the original text
