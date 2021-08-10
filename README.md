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
### 1. From PyPi
1. Run `pip install sra-downloader`

### 2. From sources
1. Download a repo into a folder
2. Run `pip install .`

## Usage
```
usage: sra-downloader [-h] [--fname FILENAME] [--save-dir SAVE_DIRECTORY] [--uncompressed [UNCOMPRESSED]] [sra_id [sra_id ...]]

Download SRA data

positional arguments:
  sra_id                SRA IDs to download

optional arguments:
  -h, --help            show this help message and exit
  --fname FILENAME      CSV file with list of SRAs to download. Header must include `Run` and `BioProject`.
  --save-dir SAVE_DIRECTORY
                        a directory that the files will be saved to. (default: ./downloaded)
  --uncompressed [UNCOMPRESSED]
                        if present, the files will not be compressed. (default: False)
```

### Examples
```
sra-downloader ERR2177760 --uncompressed
sra-downloader --fname SraRunTable.txt --save-dir ./SRAs
```

## Sample output
<!-- |-- save_folder  
&emsp;&emsp;|-- SraRunTable.txt - original SraRunTable.txt with useful metadata about samples  
&emsp;&emsp;|-- absent.txt - entries that were unaccessible due to various reasons  
&emsp;&emsp;|-- .fastq.gz - raw read archived files from SRA   -->

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