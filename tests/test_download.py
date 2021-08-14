from sra_downloader.download import download_reads, download_accession, _read_file
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
   
    
def test_single():
    save_folder = "./tests/downloaded/ERR1551967"
    download_accession("ERR1551967", 1, save_folder, False)
    assert _same_dirs(save_folder, "./tests/expected_single/ERR1551967")
    os.system(f"rm -rf {save_folder}")


def test_from_file():
    save_folder = "./tests/downloaded"
    metadata = defaultdict(list)

    with open('./tests/SraRunTable.txt', "r") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            metadata[row[1]].append(row[0])

    study_stats = download_reads(metadata, 1, save_folder, False)
    for study_name, n_samples in study_stats.items():
        tmp_save_folder = f'{save_folder}/{study_name}'
        copy2('./tests/SraRunTable.txt', f'{tmp_save_folder}')

    assert _same_dirs(save_folder, "./tests/expected")
    # os.system(f"rm -rf {save_folder}")


def test_compression():
    save_folder = "./tests/downloaded"
    metadata = defaultdict(list)
    with open('./tests/SraRunTable.txt', "r") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            metadata[row[1]].append(row[0])
    
    study_stats = download_reads(metadata, 1, save_folder, True)
    for study_name, n_samples in study_stats.items():
        tmp_save_folder = f'{save_folder}/{study_name}'
        copy2('./tests/SraRunTable.txt', f'{tmp_save_folder}')
    
    os.system(f"rm -rf {save_folder}")


def test_parse():
    with open("./tests/tmp.csv", "w") as f:
        f.write("Run,BioProject\n")
        f.write("a,b\n")
    data = _read_file("./tests/tmp.csv")
    assert dict(data) == {'b': ['a']}

    with open("./tests/tmp.csv", "w") as f:
        f.write("Run,Assay Type,AvgSpotLen,Bases,BioProject,BioSample,BioSampleModel,Bytes,Center Name,collected_by,Consent,DATASTORE filetype,DATASTORE provider,DATASTORE region,Experiment,geo_loc_name_country,geo_loc_name_country_continent,geo_loc_name,host_disease,Host,Instrument,isolation_source,lat_lon,Library Name,LibraryLayout,LibrarySelection,LibrarySource,Organism,Platform,ReleaseDate,Sample Name,SRA Study,Strain,note,sub_species,note2,Tax_ID,collection_date\n")
        f.write('SRR1655192,WGS,187,97029754,PRJNA267549,SAMN03196960,Pathogen.cl,70061188,UNIVERSITY OF WASHINGTON,UW clinical laboratory,public,"fastq,sra","gs,ncbi,s3","gs.US,ncbi.public,s3.us-east-1",SRX761658,USA,North America,USA: WA,missing,Homo sapiens,Illumina HiSeq 2000,missing,missing,10_ECLO,PAIRED,RANDOM,GENOMIC,Enterobacter cloacae,ILLUMINA,2015-07-07T00:00:00Z,10_ECLO,SRP049998,10_ECLO,,,,,\n')
    data = _read_file("./tests/tmp.csv")
    assert dict(data) == {'PRJNA267549': ['SRR1655192']}
    os.system("rm ./tests/tmp.csv")
    
def test_emptyline():

    # Creating mock test file
    with open("./tests/SraRunTable.txt", "r") as csv_in, open("./tests/test_emptyline.txt", "w", newline='') as out_csv:
        csv_reader = csv.reader(csv_in)
        csv_writer = csv.writer(out_csv)
        for row in csv_reader:
            csv_writer.writerow(row)
            
        csv_writer.writerow("\n")
    normal = _read_file("./tests/SraRunTable.txt")
    emptyline = _read_file("./tests/test_emptyline.txt")
    assert normal == emptyline 
    os.system("rm ./tests/test_emptyline.txt")

    
if __name__=="__main__":
    test_parse()