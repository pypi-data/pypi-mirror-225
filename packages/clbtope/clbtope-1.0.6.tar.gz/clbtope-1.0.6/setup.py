# setup.py

from setuptools import setup, find_packages
from setuptools import setup, Extension
from setuptools import  find_namespace_packages
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
setup(
    name='clbtope',
    version='1.0.6',
    description='CLBTope:A computational approach had been developed for predicting both types (linear/conformational) of B-cell epitopes.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license_files = ('LICENSE.txt'),
    author='Nishant Kumar',
    author_email='nishantk@iiitd.ac.in',
    url='https://github.com/raghavagps/clbtope',
    packages=find_namespace_packages(where="src"),
    package_dir={'':'src'},
    package_data={'clbtope.blast_binaries':['**/*'],
    'clbtope.blast_db':['**/*']},
    entry_points={'console_scripts' : ['clbtope = clbtope.python_scripts.clbtope:main']},
    include_package_data=True,
    python_requires='>=3.7',
    install_requires= [ 'numpy', 'pandas', 'scikit-learn', 'argparse' ,'tqdm', 'onnxruntime'
        #Add any Python dependencies here
    ]
)

