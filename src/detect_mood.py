from __future__ import print_function
from heuro_api import Heuro
from credentials import email, password

def main():
    myhero = Heuro(email, password)
    mypipe = myhero.make_pipeline(pipeline="pip1")

if __name__ == "__main__":
    main()