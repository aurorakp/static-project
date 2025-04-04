from utils import copy_and_overwrite_dir
from full_page_converters import generate_pages_recursive
import os

def main():
    copy_and_overwrite_dir(os.path.abspath('static'), os.path.abspath('public'))
    generate_pages_recursive(os.path.abspath('content'), os.path.abspath('template.html'), os.path.abspath('public'))



if __name__ == "__main__":
    main()