# setup.py

from setuptools import setup, find_packages
from setuptools import setup, Extension
from setuptools import  find_namespace_packages
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
setup(
    name='hladr4pred2',
    version='1.0.0',
    description='A computational approach to predict HLA-DRB1-04:01 binders using the sequence information of the peptides.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license_files = ('LICENSE.txt'),
    author='Sumeet patiyal',
    author_email='sumeetp@iiitd.ac.in',
    url='https://github.com/sumeetpatiyal/hladr4pred2',
    packages=find_namespace_packages(where="src"),
    package_dir={'':'src'},
    package_data={'hladr4pred2.blast_binaries':['**/*'],
    'hladr4pred2.blast_db':['**/*']},
    entry_points={'console_scripts' : ['hladr4pred2 = hladr4pred2.python_scripts.hladr4pred2:main']},
    include_package_data=True,
    python_requires='>=3.8',
    install_requires= [ 'numpy', 'pandas', 'onnxruntime', 'scikit-learn','tqdm' 
        #Add any Python dependencies here
    ]
)

