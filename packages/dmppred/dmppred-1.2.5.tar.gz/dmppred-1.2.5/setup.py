# setup.py

from setuptools import setup, find_packages
from setuptools import setup, Extension
from setuptools import  find_namespace_packages
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
setup(
    name='dmppred',
    version='1.2.5',
    description='Dmppred: A tool for predicting, designing, and scanning Type 1 associated peptides',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license_files = ('LICENSE.txt'),
    author='Nishant Kumar',
    author_email='nishantk@iiitd.ac.in',
    url='https://gitlab.com/raghavalab/dmppred',
    packages=find_namespace_packages(where="src"),
    package_dir={'':'src'},
    package_data={'dmppred.blast_binaries':['**/*'],
    'dmppred.blast_db':['**/*'],
    'dmppred.model':['*']},
    entry_points={'console_scripts' : ['dmppred = dmppred.python_scripts.dmppred:main']},
    include_package_data=True,
    python_requires='>=3.6',
    install_requires= [ 'numpy', 'pandas', 'scikit-learn', 'argparse', 'onnxruntime', 
        #Add any Python dependencies here
    ]
)
