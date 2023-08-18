from setuptools import setup, find_packages


def _get_version():
    '''
    Reads package version from file.
    '''
    version = '1.0.0'
    with open('version') as file:
        version = file.read().strip()
    return version


def _get_long_description():
    '''
    Reads long description from README.
    '''
    with open('README.md', 'r') as f:
        long_description = f.read()
    return long_description


setup(
    name='mvf',
    version=_get_version(),
    author='Tom Kim',
    author_email='tom.kim@certus-tech.com',
    description='A package implementing a supervised learning model validation framework.',
    long_description=_get_long_description(),
    long_description_content_type='text/markdown',
    packages=find_packages(
        exclude=[
            'test*',
            'documentation*',
            'examples*',
        ],
    ),
    install_requires=[
        'click',
        'feather-format',
        'matplotlib',
        'pandas',
        'ploomber',
        'rpy2',
        'rpy2-r6',
        'schema',
        'scikit-learn',
    ],
    extras_require={
        'dev': [
            'coverage',
            'pytest',
            'testbook',
            'twine',
        ]
    },
    keywords=[
        'python',
        'R',
        'machine learning',
        'validation',
        'framework',
    ],
    classifiers=[
        'Programming Language :: Python :: 3.9',
        'Framework :: Jupyter',
        'License :: Free For Educational Use',
        'Operating System :: Unix',
    ],
    python_requires='>=3.9',
    entry_points={
        'console_scripts': [
            'mvf=mvf.cli.cli:mvf'
        ]
    },
)
