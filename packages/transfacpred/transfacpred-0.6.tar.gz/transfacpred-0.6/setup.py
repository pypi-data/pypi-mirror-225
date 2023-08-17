from setuptools import setup, find_packages
from setuptools import find_namespace_packages
from pathlib import Path

# Read the contents of your README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='transfacpred',
    version='0.6',
    description='A method to predict the transcription factors using protein sequences.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license_files=('LICENSE.txt',),
    url='https://github.com/raghavagps/transfacpred',
    packages=find_namespace_packages(where="src"),
    package_dir={'':'src'},
    package_data={
        'transfacpred.blast_binaries.mac': ['*'], 
        'transfacpred.database': ['*'],
        'transfacpred.python_scripts.Models': ['*'],
    },  
    entry_points={
        'console_scripts': ['transfacpred = transfacpred.python_scripts.transfacpred:main']
    },
    include_package_data=True,
    python_requires='>=3.6',
    install_requires=[
        'numpy', 'pandas', 'scikit-learn'
    ]
)
