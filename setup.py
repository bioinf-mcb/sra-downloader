from setuptools import setup
import pathlib

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(name='sra-downloader',
        version='1.0.1',
        description='A script for batch-downloading and automatic compression of data from NCBI Sequence Read Archive. Built on SRA-Toolkit.',
        long_description=README,
        long_description_content_type="text/markdown",
        author='Valentyn Bezshapkin & Witold Wydmański',
        author_email='witold.wydmanski@uj.edu.pl',
        url='https://github.com/bioinf-mcb/sra-downloader',
        packages=['sra_downloader'],
        license="MIT",
        entry_points = {
            'console_scripts': [
                'sra-downloader=sra_downloader.__main__:main',
            ],
        }
     )