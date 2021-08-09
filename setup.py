from distutils.core import setup

setup(name='sra-downloader',
        version='1.0',
        description='Python Distribution Utilities',
        author='Valentyn Bezshapkin & Witold Wydmański',
        author_email='witold.wydmanski@uj.edu.pl',
        url='https://github.com/bioinf-mcb/sra-downloader',
        packages=['sra_downloader'],
        entry_points = {
            'console_scripts': [
                'sra-downloader=sra_downloader.__main__:main',
            ],
        }
     )