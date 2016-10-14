from __future__ import print_function
from heuro_api import Heuro

def main():
    myhero = Heuro()
    mypipe = myhero.make_pipeline(pipeline="pip1")

if __name__ == "__main__":
    main()