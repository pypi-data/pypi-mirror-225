from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Intended Audience :: Developers',
    'Operating System :: Microsoft :: Windows',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Operating System :: Unix',
    'Operating System :: iOS',
]
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='eganetswahilicleaner',
    version='0.0.2',
    description='SWAHILI TEXT CLEANING LIBRARY FOR NATURAL LANGUAGE PROCESSING',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='',
    author='Shadrack Kajigili',
    author_email='shadrackkajigili4@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='swahili_text_cleaner',
    packages=find_packages(),
    install_requires=['nltk']
)