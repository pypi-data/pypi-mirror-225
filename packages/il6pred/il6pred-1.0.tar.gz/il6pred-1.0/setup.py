from setuptools import setup, find_packages
from setuptools import find_namespace_packages
from pathlib import Path
import joblib

# Read the contents of your README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='il6pred',
    version='1.0',
    description='A method for predicting and designing IL-6 inducing peptides.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license_files=('LICENSE.txt',),
    url='https://github.com/raghavagps/il6pred',
    packages=find_namespace_packages(where="src"),
    package_dir={'': 'src'},
    package_data={
        'il6pred.Models': ['*'],
        'il6pred.Data': ['*']
    }, 
    entry_points={'console_scripts': ['il6pred = il6pred.python_scripts.il6pred:main']},
    include_package_data=True,
    python_requires='<=3.7.16',
    install_requires=[
        'pandas==1.1.5', 'scikit-learn<=0.21.3'
    ]
)

