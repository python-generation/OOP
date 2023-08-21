import os
from zipfile import ZipFile

from more_itertools import chunked


def create_test_files(archive, extract_path):
    if not os.path.exists(extract_path):
        os.mkdir(extract_path)

    with (
        ZipFile(f'{archive}') as zf,
        open(f'{extract_path}/input.txt', 'w', encoding='utf-8') as inp,
        open(f'{extract_path}/output.txt', 'w', encoding='utf-8') as out
    ):
        files_pairs = chunked(zf.namelist(), 2)
        inp.write('# INPUT DATA:\n\n')
        out.write('# OUTPUT DATA:\n\n')
        test_number = 1
        for reply, clue in files_pairs:
            with zf.open(reply) as f_reply, zf.open(clue) as f_clue:
                inp.writelines(f'# TEST_{test_number}:\n{f_reply.read().decode()}\n\n')
                out.writelines(f'# TEST_{test_number}:\n{f_clue.read().decode()}\n\n')
                test_number += 1


def scan_dir(path):
    for i in os.listdir(path):
        directory = path + '/' + i
        if directory.endswith('.zip'):
            extract_path, zip_file = os.path.split(directory)
            module_number = f"{extract_path.split('/')[-1]}.{zip_file.split('.')[0]}"
            mkdir = f'{extract_path}/{module_number}'
            create_test_files(directory, mkdir)
        if os.path.isdir(path + '/' + i):
            scan_dir(path + '/' + i)


if __name__ == '__main__':
    path = '.'
    scan_dir(path)