import os
from shutil import copy2
import sys
import json
import subprocess, shlex
import logging
import glob
from collections import defaultdict
import csv
from pathlib import Path

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logger = logging.getLogger('SRA-downloader')

# log files loading functions
def _load_log(filepath):
    """ Opens or creates new log file"""
    try:
        with open(filepath) as l:
            log = json.load(l)
    except FileNotFoundError:
        log = {}
    return log

def _find_processed(directory):
    processed = glob.glob("{0}/*.sr*.fast*".format(directory))
    processed = [os.path.split(i)[-1].split(".")[0] for i in processed]
    return processed

def _load_absent(filepath):
    """ Opens or creates DataFrame with absent files"""
    res = []
    with open(filepath, "r") as f:
        res = f.readlines()
    res = [i.strip() for i in res]
    return res

def _call(command):
    res = subprocess.run(command, shell=True, capture_output=True, universal_newlines=True)
    if res.stderr:
        logger.error(res.stderr)
    return res

def download_accession(accession, cores, save_folder="./downloaded", compress=True):
    """ Downloads a single accession file to the target directory
    
    Args:
        accession (str): run accession
        save_folder (str): target directory
        compress (bool): if `True`, the file will be in the `fastq.gz` format
    """

    fname = os.path.join(save_folder, accession)

    prefetch = "prefetch --max-size 100G " + accession + " -o " + fname + ".sra"
    results = _call(prefetch)
    if "no data" in str(results.stderr):
        logger.error("Accession {0} not found".format(accession))
        raise FileNotFoundError

    fasterq_dump = "fasterq-dump {0}.sra -O {1}".format(fname, save_folder)
    res = _call(fasterq_dump)
    if 'invalid accession' in res.stderr:
        logger.warning('Accession {0} not found'.format(accession))
        raise FileNotFoundError 

    os.remove(fname + '.sra')
    if compress:
        for fname in glob.glob("{0}/{1}*.fastq".format(save_folder, accession)):
            compress = 'pigz '
            if cores is not None:
                compress += ' -p ' + str(cores)
            compress += ' ' + fname
            _call(compress)


def download_reads(metadata, cores, save_folder, compress=True, skip_absent=True):
    """ Downloads a list of accessions and puts them into project directories.
    
    Args:
        metadata (dict): dictionary with bioproject names as keys and SRA IDs as list of values.
            The keys don't have to be real bioproject identifiers.
        save_folder (str): root target directory
        compress (bool): if `True`, the file will be in the `fastq.gz` format
        skip_absent (bool): if `True`, skip the files that couldn't be downloaded earlier

    Returns:
        dict: info about how many SRAs were downloaded for each project
    """

    study_stats = {}
    processed_no = 1
    all_accessions = [item for sublist in metadata.values() for item in sublist]

    for study_name, accessions in metadata.items():
        study_save_folder = os.path.join(save_folder, study_name)
        processed = _find_processed(study_save_folder)

        try:
            absent = _load_absent(os.path.join(study_save_folder, "absent.txt"))
        except FileNotFoundError:
            absent = []
        
        for sra_id in accessions:
            fname = os.path.join(save_folder, sra_id)

            logger.info("Currently processing: " + sra_id + " ({0}/{1})".format(processed_no, len(all_accessions)))
            processed_no += 1

            if sra_id in processed:
                logger.info("Already present! Skipping.")
                continue
            if skip_absent:
                if sra_id in absent:
                    logger.info("Absent! Skipping.")
                    continue

            try:
                download_accession(sra_id, cores, '{0}/{1}'.format(save_folder, study_name), compress)
            except FileNotFoundError:
                Path(study_save_folder).mkdir(parents=True, exist_ok=True)

                with open(os.path.join(study_save_folder, "absent.txt"), "a") as f:
                    f.write(sra_id+"\n")

            if not study_name in study_stats.keys():
                study_stats[study_name] = 1
            else:
                study_stats[study_name] += 1

    return study_stats

def _read_file(fname):
    def __find_index(list, name):
        return [i for i in range(len(header)) if list[i]==name][0]

    metadata = defaultdict(list)
    with open(fname, "r") as f:
        reader = csv.reader(f)
        header = next(reader)
        project_idx = __find_index(header, "BioProject")
        run_idx = __find_index(header, "Run")

        try:
            for row in reader:
                metadata[row[project_idx]].append(row[run_idx])
        # workaround for empty line in the file 
        except IndexError:
            pass

    return metadata

if __name__ == "__main__":  
    # Change this to your download location
    save_folder = "./downloaded"

    # input path to your SraRunTable.txt from the study
    # metadata = pd.read_csv('SraRunTable.txt')
    
    study_stats = download_reads(metadata, save_folder)
    # Moving meta SraRunTable to study folder

    # Adding final output
    for study_name, n_samples in study_stats.items():
        tmp_save_folder = '{0}/{1}'.format(save_folder, study_name)
        copy2('SraRunTable.txt', tmp_save_folder)
        logger.info('{0} sample from {1} downloaded'.format(n_samples, study_name))
