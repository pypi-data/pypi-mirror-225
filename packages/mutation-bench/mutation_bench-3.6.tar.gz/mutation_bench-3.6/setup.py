from setuptools import setup, find_packages
from setuptools import  find_namespace_packages
# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='mutation_bench',
    version='3.6',
    description='A tool for Prediction of high-risk cancer patients using mutation profiles',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license_files = ('LICENSE.txt',),
    url='https://github.com/raghavagps/mutation_bench', 
    packages=find_namespace_packages(where="src"),
    package_dir={'':'src'},
    package_data={'mutation_bench.perl_scripts':['*']
    },
    entry_points={ 'console_scripts' : ['mutation_bench = mutation_bench.muthrp:main']},
    include_package_data=True,
    python_requires='>=3.6',
    install_requires=[
        'numpy', 'pandas', 'rpy2', 'xgboost', 'scikit-learn', 'tqdm',  # Add any Python dependencies here
    ]
)
