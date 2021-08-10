from .download import download_accession, download_reads, _find_processed, _read_file
import argparse
import glob
from collections import defaultdict
import csv

def str2bool(v):
    print(v)
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def main():
    parser = argparse.ArgumentParser(description='Download SRA data and organize them by projects')
    parser.add_argument('accessions', metavar='sra_id', type=str, nargs='*', default=[],
                        help='SRA IDs to download')
    parser.add_argument('--fname', dest='filename', default=None, type=str,
                        help='CSV file with list of SRAs to download. Header must include `Run` and `BioProject`.')
    parser.add_argument('--save-dir', dest='save_directory', default='./downloaded', type=str,
                    help='a directory that the files will be saved to. (default: ./downloaded)')
    parser.add_argument('--uncompressed', type=str2bool, nargs="?", help="if present, the files will not be compressed. (default: False)", default=False, const=True)

    args = parser.parse_args()
    if args.filename is None and len(args.accessions)==0:
        parser.print_help()
        return

    processed = _find_processed(args.save_directory)
    for sra_id in args.accessions:
        print("Processing:", sra_id)
        if sra_id in processed:
            print("Already processed, skipping.")
            continue
        download_accession(sra_id, args.save_directory, not args.uncompressed)

    if args.filename is not None:
        metadata = _read_file(args.filename)
        download_reads(metadata, args.save_directory, not args.uncompressed)

if __name__=="__main__":
    main()