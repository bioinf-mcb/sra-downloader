# sra-downloader
A script for batch-downloading data from NCBI Sequence Read Archive built on SRA-Toolkit

# Requirements
- python >= 3.6
- sra-toolkit == 2.10.9
- pigz 

# How to use it? 
1. Download a repo into a folder
2. Configure **download.py**
- Add SRA-Toolkit path on line 77 
- Add download folder path on line 80   
3. Replace **SraRunTable.txt** with **SraRunTable.txt** from desired study (available as "Metadata" file from SRA Run Selector)
4. Run download.py

# Output
|-- save_folder
    |-- SraRunTable.txt         - original SraRunTable.txt with useful metadata about samples
    |-- absent.txt              - entries that were unaccessible due to various reasons
    |-- .fastq.gz               - files from SRA

# Multiple study download
1. Copy a folder with configured download.py
2. Replace **SraRunTable.txt** with **SraRunTable.txt** from desired study
3. Run download.py
4. Repeat! 
