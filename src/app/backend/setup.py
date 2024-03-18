from setuptools import setup, find_packages

# setup.py is used to configure various aspects of your package like metadata,
# dependencies, and more. It's an essential part of making your package installable
# and distributable. The 'setup' function call below specifies how this package
# will be installed and its metadata.
setup(
    name="api",
    version="0.1",
    packages=find_packages(),
    description="A Python API package that provided class to interact with CS-cart API",
    author="Bhavesh Choudhary",
    author_email="probhavsh@gmail.com",
    url="https://github.com/proBhavesh/",
)
