import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='func_adl_uproot',
    version='2.0.0',
    description=(
        'Functional Analysis Description Language'
        + ' uproot backend for accessing flat ROOT ntuples'
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(exclude=['tests']),
    python_requires=('>=3.8, <3.12'),
    install_requires=[
        'awkward>=2.0.9',
        'dask[complete]',
        'dask-awkward>=2023.8.1',
        'func-adl>=3.1',
        'numpy',
        'qastle>=0.16.0',
        'uproot>=5',
        'vector>=1.1.0',
    ],
    extras_require={'test': ['flake8', 'pytest', 'pytest-cov']},
    author='Mason Proffitt',
    author_email='masonlp@uw.edu',
    url='https://github.com/iris-hep/func_adl_uproot',
)
