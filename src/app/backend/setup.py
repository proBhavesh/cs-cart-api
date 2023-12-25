from setuptools import setup, find_packages

setup(
    name="api", 
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        # Include the global_data.py file from any package
        '': ['global_data.py'],
    },
    description="A Python API package that provided class to interact with CS-cart API",
    author="Bhavesh Choudhary",
    author_email="probhavsh@gmail.com",
    url="https://github.com/proBhavesh/",  # if your project is hosted on GitHub
)
