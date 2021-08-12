# sra-downloader
A script for batch-downloading and automatic compression of data from NCBI Sequence Read Archive. Built on SRA-Toolkit.

Features:
 - Downloading SRAs using either accession IDs or NCBI generated files
 - Organizing sequences by projects that they come from
 - Detecting which runs have been already downloaded

## Requirements
- python >= 3.6
- sra-toolkit >= 2.9.6
- pigz 

## Instalation
### 0. Docker
1. Run `docker run wwydmanski/sra-downloader -h`

### 1. Conda (recommended, also downloads sra-toolkit)
1. Run `conda install -c bioconda -c bioinf-mcb sra-downloader` 

Note: if you don't specify the `bioconda` channel you will get a dependency error.

### 2. From PyPi
1. Run `pip install sra-downloader`

### 3. From sources
1. Download a repo into a folder
2. Run `pip install .`

## Usage
```
usage: sra-downloader [-h] [--fname FILENAME] [--save-dir SAVE_DIRECTORY] [--uncompressed [UNCOMPRESSED]] [--cores [CORES]] [sra_id [sra_id ...]]

Download SRA data and organize them by projects

positional arguments:
  sra_id                SRA IDs to download

optional arguments:
  -h, --help            show this help message and exit
  --fname FILENAME      CSV file with list of SRAs to download. Header must include `Run` and `BioProject`.
  --save-dir SAVE_DIRECTORY
                        a directory that the files will be saved to. (default: ./downloaded)
  --uncompressed [UNCOMPRESSED]
                        if present, the files will not be compressed. (default: False)
  --cores [CORES]       Cores used for compression. (default is the number of online processors, or 8 if unknown)
```

### Examples
```
sra-downloader ERR2177760 --uncompressed
docker run -v $(pwd)/downloads:/downloaded wwydmanski/sra-downloader ERR1551967
sra-downloader --fname SraRunTable.txt --save-dir ./SRAs --cores 4
```

## Sample output

```
└─── save_folder
    ├── PRJEB14961
    │   ├── ERR1551967.sra_1.fastq.gz  # - raw read archived files from SRA
    │   ├── ERR1551967.sra_2.fastq.gz 
    │   └── SraRunTable.txt            # - original SraRunTable.txt with useful metadata about samples  
    └── PRJEB20463
        ├── ERR2177760.sra_1.fastq.gz
        ├── ERR2177760.sra_2.fastq.gz 
        ├── absent.txt                 # - entries that were unaccessible due to various reasons
        └── SraRunTable.txt
```