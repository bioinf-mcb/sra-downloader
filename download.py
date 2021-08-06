import subprocess
import pandas as pd
import os
from shutil import copy2
import sys
import json


# log files loading functions
def load_log(filepath):
    """ Opens or creates new log file"""
    try:
        with open('log.txt') as l:
            log = json.load(l)
    except FileNotFoundError:
        log = {}
    return log


def load_absent(filepath):
    """ Opens or creates DataFrame with absent files"""
    try:
        absent = pd.read_csv('absent.txt')
    except FileNotFoundError:
        absent = pd.DataFrame(columns=metadata.columns)
    return absent


def download_reads(metadata, save_folder):
    # Iterating through rows of metadata dataframe
    study_stats = {}
    for row in metadata.itertuples():
        log = load_log("log.txt")
        absent = load_absent("absent.txt")
        sra_id = row.Run
        study_name = row.BioProject
        study_save_folder = os.path.join(save_folder, study_name)
        # prefetch
        if sra_id not in log.keys() and sra_id not in absent.Run.values:
            print(f'Files left: {len(metadata) - len(log) - len(absent)}')
            print("Currently downloading: " + sra_id)
            prefetch = "prefetch --max-size 100G " + sra_id + " -o " + sra_id + ".sra"
            results = subprocess.run(prefetch, shell=True, capture_output=True)
            if not "no data ( 404 )" in str(results.stderr):
                # unpack .sra
                print("Currently unpacking: " + sra_id)
                # Change saving path
                fasterq_dump = f"fasterq-dump {sra_id}.sra -O {study_save_folder}"
                subprocess.run(fasterq_dump, shell=True, capture_output=True)
                log[sra_id] = 1
                os.remove(sra_id + '.sra')
                # Change saving path
                for folder, _, filenames in os.walk(f'{study_save_folder}'):
                    for filename in filenames:
                        if filename.endswith('.fastq'):
                            subprocess.run('nice -n 10 pigz ' + os.path.join(folder, filename),
                                           shell=True, capture_output=True)
                with open('log.txt', 'w') as out:
                    json.dump(log, out)

            else:
                # Saves absent files to .csv
                absent = absent.append(metadata[metadata.Run == sra_id])
                absent.to_csv('absent.txt', sep=',', index=False)

        if not study_name in study_stats.keys():
            study_stats[study_name] = 1
        else:
            study_stats[study_name] += 1

    return study_stats


if __name__ == "__main__":
    sys.path.append('/path-to-sra-tools/sra-tools/sratoolkit.2.10.9-ubuntu64/bin/')
    # input path to your SraRunTable.txt from the study
    metadata = pd.read_csv('SraRunTable.txt')
    save_folder = "./dow_data"
    study_stats = download_reads(metadata, save_folder)
    # Moving meta SraRunTable to study folder

    # Adding final output
    for study_name, n_samples in study_stats.items():
        save_folder = f'/storage/BINF/TomaszLab/gmhi/wgs/{study_name}/'
        copy2('SraRunTable.txt', f'{save_folder}')
        print(f'{n_samples} from {study_name} downloaded!')

    if len(metadata) == len(log) + len(absent):
        os.remove('SraRunTable.txt')
        copy2('absent.txt', f'{save_folder}')
        os.remove('absent.txt')
