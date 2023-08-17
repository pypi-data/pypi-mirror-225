import sys
# sys.path.append("..src/")
from src import dran

def test_hello_no_params():
    assert dran.say_hello() == "Hello, World!"

def test_hello_with_params():
    assert dran.say_hello('Pfesi') == "Hello, Pfesi!"   