import setuptools

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name='sharejeeni',
    version='1.0.1',
    author='Jeevan V',
    author_email='jeevanvsan@gmail.com',
    description='Download files from sharepoint site using client id , client secret and tenant id via Azure Active Directory. ',
    long_description = long_description,
    long_description_content_type="text/markdown",  
    packages= setuptools.find_packages(),
    keywords=['sharejeeni', 'sharepoint','sharepoint file'],
    classifiers=[
    "Programming Language :: Python :: 3" ,
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    ],
)

