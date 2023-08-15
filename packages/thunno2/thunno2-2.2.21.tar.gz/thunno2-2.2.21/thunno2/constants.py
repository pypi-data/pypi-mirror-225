import datetime
import math
from string import *

from thunno2.codepage import *
from thunno2.version import *

"""
Constants in Thunno start with a `k` and then have one other character after that.
This is the dictionary where all the constants are defined
"""

CONSTANTS = {
    "A": ascii_uppercase,
    "B": "Buzz",
    "C": CODEPAGE,
    "D": "0123456789",
    "E": math.e,
    "F": "Fizz",
    "G": (1 + 5**0.5) / 2,
    "H": "Hello, World!",
    "I": (lambda: datetime.datetime.now().microsecond),
    "J": (lambda: datetime.datetime.now().second),
    "K": (lambda: datetime.datetime.now().minute),
    "L": (lambda: datetime.datetime.now().hour),
    "M": (lambda: datetime.datetime.now().day),
    "N": (lambda: datetime.datetime.now().month),
    "O": (lambda: datetime.datetime.now().year),
    "P": math.pi,
    "Q": (lambda: str(datetime.datetime.now()).split(".")[0]),
    "R": "()[]{}",
    "S": "([{",
    "T": ")]}",
    "U": "([{<",
    "V": ")]}>",
    "W": "AEIOU",
    "X": "BCDFGHJKLMNPQRSTVWXYZ",
    "Y": "AEIOUY",
    "Z": "BCDFGHJKLMNPQRSTVWXZ",
    "a": ascii_lowercase + ascii_uppercase,
    "b": "buzz",
    "c": "".join("%c" * 95 % (*range(32, 127),)),
    "d": "01",
    "e": "01234567",
    "f": "0123456789ABCDEF",
    "g": ["Fizz", "Buzz"],
    "h": "Hello World",
    "i": 16,
    "j": 32,
    "k": 64,
    "l": 128,
    "m": 256,
    "n": 512,
    "o": 1024,
    "p": 2048,
    "q": 4096,
    "r": 8192,
    "s": 16384,
    "t": 32768,
    "u": 65536,
    "v": ["qwertyuiop", "asdfghjkl", "zxcvbnm"],
    "w": "aeiou",
    "x": "bcdfghjklmnpqrstvwxyz",
    "y": "aeiouy",
    "z": "bcdfghjklmnpqrstvwxz",
    "1": 10**3,
    "2": 10**4,
    "3": 10**5,
    "4": 10**6,
    "5": 10**7,
    "6": 10**8,
    "7": 10**9,
    "8": 10**10,
    "9": 10**11,
    "0": 10**12,
    "!": THUNNO_VERSION,
    '"': [0, 0],
    "#": [0, 1],
    "$": [0, -1],
    "%": [1, 0],
    "&": [1, 1],
    "'": [1, -1],
    "(": [-1, 0],
    ")": [-1, 1],
    "*": [-1, -1],
    "+": [3, 5],
    ",": "AEIOUaeiou",
    "-": "aeiouAEIOU",
    ".": "AEIOUYaeiouy",
    "/": "aeiouyAEIOUY",
    "Ȧ": ascii_lowercase + ascii_uppercase + "0123456789",
    "Ḃ": "0123456789" + ascii_uppercase + ascii_lowercase,
    "Ċ": ascii_lowercase + ascii_uppercase + "0123456789_",
    "Ḋ": ascii_uppercase[::-1],
    "Ė": ascii_lowercase[::-1] + ascii_uppercase[::-1],
    "Ḟ": ascii_lowercase[::-1] + ascii_uppercase[::-1] + "9876543210_",
    "Ġ": ascii_uppercase + ascii_lowercase,
    "Ḣ": ascii_uppercase[::-1] + ascii_lowercase[::-1],
    "İ": ascii_lowercase[::-1] + ascii_uppercase[::-1] + "9876543210",
    "Ŀ": ascii_uppercase + ascii_lowercase + "0123456789",
    "Ṁ": ascii_uppercase[::-1] + ascii_lowercase[::-1] + "9876543210",
    "Ṅ": "9876543210",
    "Ȯ": "\n" + "".join("%c" * 95 % (*range(32, 127),)),
    "Ṗ": punctuation,
    "Ṙ": "http://",
    "Ṡ": "http://www.",
    "Ṫ": "https://www.",
    "Ẇ": whitespace,
    "Ẋ": ["()", "[]", "{}", "<>"],
    "Ẏ": "([{<>}])",
    "Ż": "[]<>-+.,",
}
