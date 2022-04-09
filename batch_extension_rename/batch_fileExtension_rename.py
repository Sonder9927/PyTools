# batch_fileExtension_rename.py
# created: 4th April 2022

'''
This will batch rename a group of files in given directory,
once you pass the current and new extensionsor.
'''

'''
python batch_fileExtension_rename.py renamtest py js

or
python batch_fileExtension_rename.py renamtest .py .js
'''

# just checking
_author_ = 'Sonder M. W.'
_version_ = '1.0.2'

from icecream import ic
import argparse
import os

def batch_rename(work_dir, old_ext, new_ext):
    for filename in os.listdir(work_dir):
        # Get the file extension
        split_file = os.path.splitext(filename)
        # unpack tuple element
        root_name, file_ext = split_file
        # start of the logic to check the file extensions, if old_ext == file_ext
        if old_ext == file_ext:
            # Return changed name of the file with new extention
            newfile = root_name + new_ext

            # Writes the files
            os.rename(os.path.join(work_dir, filename), os.path.join(work_dir, newfile))
    #print('rename is done')
    #print(os.listdir(work_dir))
    ic('rename is done')
    ic(os.listdir(work_dir))


def get_parser():
    parser = argparse.ArgumentParser(
        description = "change extension of files in a work directory"
    )
    parser.add_argument(
        'work_dir',
        metavar = 'WORK_DIR',
        type = str,
        nargs = 1,
        help = 'the directory where to change extension',
    )
    parser.add_argument(
        'old_ext', metavar='OLD_EXT', type=str, nargs=1, help='old extension'
    )
    parser.add_argument(
        'new_ext', metavar='NEW_EXT', type=str, nargs=1, help='new extension'
    )
    return parser

def main():
    '''
    This will be called if the script is directly invoked.
    '''
    # adding commend line argument
    parser = get_parser()
    args = vars(parser.parse_args())

    # Set the variable work_dir with the first argument passed
    work_dir = args["work_dir"][0]
    # Set the variable old_ext with the second argument passed
    old_ext = args["old_ext"][0]
    if old_ext and old_ext[0] != '.':
        old_ext = '.' + old_ext
    # Set the variable new_ext with the third argument passed
    new_ext = args["new_ext"][0]
    if new_ext and new_ext[0] != '.':
        new_ext = '.' + new_ext

    batch_rename(work_dir, old_ext, new_ext)


if __name__ == "__main__":
    main()


