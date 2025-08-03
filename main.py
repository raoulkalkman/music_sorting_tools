#!~/bin/python3

'''Simple script which:
recursively moves all files in pioneer/Contents folder to 
separate directory with a flattened structure

* meant to be run from the command line
* meant to be used for traktor analysis of pioneer FS

@author Raoul Kalkman
@date 16 may 2025
'''
import click
import os
import shutil

def _get_free_space(path: str) -> int:
    '''Get the free space (in bytes) of a directory'''
    statvfs = os.statvfs(path)
    return statvfs.f_frsize * statvfs.f_bavail

def _get_total_size(path: str) -> int:
    '''Get the total size (in bytes) of all files in a directory'''
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is a symlink
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return total_size

@click.command()
@click.argument('pioneer', nargs=1)
@click.argument('output', nargs=1)
def run(pioneer: str, output: str):
    '''Main functionality, 
    PRE: pioneer is a path to the "Contents" folder of pioneer
    
    copies files recursively from pioneer folder to output
    creates output folder if not existent'''

    # Check input arguments
    if not os.path.exists(pioneer):
        raise FileNotFoundError(f'Pioneer folder {pioneer} does not exist')
    
    if os.path.basename(os.path.normpath(pioneer)) != "Contents":
        raise ValueError(f"The last folder in the path '{pioneer}' is not 'Contents'.")

    if not os.path.exists(output):
        os.makedirs(output)
        print(f"Output folder '{output}' created.")

    # Check if there is enough space in the output folder
        
    required_size: int  = _get_total_size(pioneer)
    free_space: int     = _get_free_space(output)
    
    if required_size > free_space:
        raise ValueError(
            f"Not enough space in output folder '{output}' to copy files from '{pioneer}'.\nRequired size: {required_size} bytes, free space: {free_space} bytes."
            )

    # Get all files in the pioneer folder
    for dirpath, dirnames, filenames in os.walk(pioneer):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is a symlink
            if not os.path.islink(fp):
                # Copy file to output folder (flatten structure)
                dest = os.path.join(output, os.path.basename(fp))
                base, ext = os.path.splitext(dest)
                counter = 2
                # If file exists, add _2, _3, etc.
                while os.path.exists(dest):
                    dest = f"{base}_{counter}{ext}"
                    counter += 1
                shutil.copy2(fp, dest)
                print(f"Copied {fp} to {dest}")


if __name__ == "__main__":
    try:
        run()
        exit(0)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
