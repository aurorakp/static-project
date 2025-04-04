import os
import shutil

def copy_and_overwrite_dir(start, target):
    print(f'copying {start} to {target}')
    print(f'{start} has: ')
    print(f'{os.listdir(start)}')
    print(f'checking for {target} existence...')
    if os.path.exists(target):
        print(f'{target} exists, deleting')
        print(f'{os.listdir(target)}')
        shutil.rmtree(target)

    shutil.copytree(start, target)
    print('new target dir contents: ')
    print(f'{os.listdir(target)}')
    print("Copy successful")
