from setuptools import setup, find_packages

setup(
    name='rggrader',
    version='0.1.1',
    description='Submisiion tool for REA course',
    author='Aditira Jamhuri',
    author_email='aditira.jamhuri@ruangguru.com',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)