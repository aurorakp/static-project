import os
import shutil
import sys

from full_page_converters import generate_pages_recursive

static_path = "./static"
public_path = "./docs"
content_path = "./content"
template_path = "./template.html"



def main():
    basepath = '/'
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    print(f'basepath is: {basepath}')
    if os.path.exists(public_path):
        shutil.rmtree(public_path)

    shutil.copytree(static_path, public_path)

    generate_pages_recursive(content_path, template_path, public_path, basepath)
    

if __name__ == "__main__":
    main()