import setuptools

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name='pysharepi',
    version='1.5',
    author='Jeevan V',
    author_email='jeevanvsan@gmail.com',
    description='Download files from sharepoint site using client id , client secret and tenant id via Azure Active Directory. ',
    long_description = long_description,
    long_description_content_type="text/markdown",  
    packages= setuptools.find_packages(),
    classifiers=[
    "Programming Language :: Python :: 2" ,
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    ],
)

