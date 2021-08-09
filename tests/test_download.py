from sra_downloader.download import download_reads, download_accession
from shutil import copy2
import filecmp
import os
import csv
from collections import defaultdict

def _same_dirs(a, b):
    """Check that structure and files are the same for directories a and b

    Args:
        a (str): The path to the first directory
        b (str): The path to the second directory
    """
    comp = filecmp.dircmp(a, b)
    common = sorted(comp.common)
    left = sorted(comp.left_list)
    right = sorted(comp.right_list)

    if left != common or right != common:
        raise AssertionError(str(comp.common))
    if len(comp.diff_files):
        raise AssertionError(str(comp.diff_files))
    for fname in common:
        if fname in comp.common_dirs:
            continue
        left_file = os.path.join(a, fname)
        right_file = os.path.join(b, fname)
        assert filecmp.cmp(left_file, right_file), fname
    for subdir in comp.common_dirs:
        left_subdir = os.path.join(a, subdir)
        right_subdir = os.path.join(b, subdir)
        return _same_dirs(left_subdir, right_subdir)
    return True 

def test_from_file():
    save_folder = "./tests/downloaded"
    metadata = defaultdict(list)

    with open('./tests/SraRunTable.txt', "r") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            metadata[row[1]].append(row[0])

    study_stats = download_reads(metadata, save_folder, False)
    for study_name, n_samples in study_stats.items():
        tmp_save_folder = f'{save_folder}/{study_name}'
        copy2('./tests/SraRunTable.txt', f'{tmp_save_folder}')

    assert _same_dirs(save_folder, "./tests/expected")
    os.system(f"rm -rf {save_folder}")

def test_compression():
    save_folder = "./tests/downloaded"

    metadata = pd.read_csv('./tests/SraRunTable.txt')
    
    study_stats = download_reads(metadata, save_folder, True)
    for study_name, n_samples in study_stats.items():
        tmp_save_folder = f'{save_folder}/{study_name}'
        copy2('./tests/SraRunTable.txt', f'{tmp_save_folder}')
    
    os.system(f"rm -rf {save_folder}")

def test_single():
    save_folder = "./tests/downloaded/ERR1551967"
    download_accession("ERR1551967", save_folder, False)
    assert _same_dirs(save_folder, "./tests/expected_single/ERR1551967")
    os.system(f"rm -rf {save_folder}")

if __name__=="__main__":
    test_from_file()