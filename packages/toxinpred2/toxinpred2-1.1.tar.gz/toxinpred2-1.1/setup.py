from setuptools import setup, find_packages
from setuptools import  find_namespace_packages
# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='toxinpred2',
    version='1.1',
    description='A tool to predict toxic and non-toxic proteins',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license_files = ('LICENSE.txt',),
    url='https://github.com/raghavagps/toxinpred2', 
    packages=find_namespace_packages(where="src"),
    package_dir={'':'src'},
    package_data={ 'toxinpred2.blast_binaries':['**/*'],
	'toxinpred2.Database':['*'],
	'toxinpred2.model':['*'],
    
    'toxinpred2.progs':['*']},
    entry_points={ 'console_scripts' : ['toxinpred2 = toxinpred2.python_scripts.toxinpred2:main']},
    include_package_data=True,
    python_requires='>=3.6',
    install_requires=[
        'numpy', 'pandas' , 'argparse', 'joblib', 'onnxruntime' # Add any Python dependencies here
    ]
)
