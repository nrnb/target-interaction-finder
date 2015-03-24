from setuptools import setup, find_packages  # Always prefer setuptools over distutils
from codecs import open  # To use a consistent encoding
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='exrnamapper',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='0.0.1',

    description='Map exRNA to proteins',
    #long_description=long_description,

    # The project's main homepage.
    url='https://github.com/ariutta/exrna-mapper',

    # Author details
    author='Anders Riutta',
    #author_email='',

    # Choose your license
    license='Apache2',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Biologists',
        'Topic :: Computational Biology :: Bioinformatics',

        # Pick your license as you wish (should match "license" above)
        'License :: Apache2',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        '''
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        '''
    ],

    # What does your project relate to?
    keywords='Network Biology, Biological Pathways',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),

    # List run-time dependencies here.  These will be installed by pip when your
    # project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    #install_requires=['numpy==1.9.2', 'scipy==0.15.1', 'networkx==1.9.1', 'networkxgmml==0.1.3'],
    # The above is commented out, because the version of networkxgmml on PyPi throws an error
    # when parsing XGMML files from Genboree.
    # Until the pull request
    # https://github.com/informationsea/networkxxgmml/pull/1
    # is accepted, you need to install the dependencies without networkxgmml:
    install_requires=['numpy==1.9.2', 'scipy==0.15.1', 'networkx==1.9.1'],
    # And then install the ariutta fork of networkxgmml like this:
    # pip install https://github.com/ariutta/networkxxgmml/zipball/master

    # List additional groups of dependencies here (e.g. development dependencies).
    # You can install these using the following syntax, for example:
    # $ pip install -e .[dev,test]
    extras_require={
        #'dev': ['check-manifest'],
        #'test': ['mock'],
    },

    entry_points={
        #'console_scripts': [
        #    'exrnamapper=exrnamapper:main',
        #],
    },
)
