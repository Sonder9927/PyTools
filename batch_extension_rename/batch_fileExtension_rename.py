# batch_fileExtension_rename.py
# author: Sonder M. W.
# created: 4th April 2022
# version: 0.0.3

from icecream import ic
from pathlib import Path
import argparse

'''
This will batch rename a group of files in given directory,
once you pass the current and new extensionsor.

`python batch_fileExtension_rename.py renamtest py js`
or
`python batch_fileExtension_rename.py renamtest .py .js`
'''

def batch_rename(work_dir: Path, old_ext: str, new_ext: str) -> None:
    # default is glob
    # targets = work_dir.rglob(f'*{old_ext}')
    targets = work_dir.glob(f'*{old_ext}')
    ic("Renaming")
    for target in targets:
        # Get the name without suffix
        newfile = target.parent / f"{target.stem}{new_ext}"
        target.rename(newfile)

        # print info
        info = f"{target} -> {newfile}"
        ic(info)

    ic('Renaming is done.')


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
    work_dir = Path(args["work_dir"][0])

    # Set the variable old_ext with the second argument passed
    old_ext = args["old_ext"][0]

    # Set the variable new_ext with the third argument passed
    new_ext = args["new_ext"][0]
    if new_ext and new_ext[0] != '.':
        new_ext = '.' + new_ext

    batch_rename(work_dir, old_ext, new_ext)


if __name__ == "__main__":
    main()

