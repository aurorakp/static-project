import os
import sys

from full_page_converters import generate_pages_recursive
from utils import copy_and_overwrite_dir


def main():
    basepath = sys.argv[0]
    if basepath == "":
        basepath = '/'
    copy_and_overwrite_dir(os.path.abspath('static'), os.path.abspath('docs'))
    generate_pages_recursive(os.path.abspath('content'), os.path.abspath('template.html'), os.path.abspath('docs'), basepath)
    

if __name__ == "__main__":
    main()