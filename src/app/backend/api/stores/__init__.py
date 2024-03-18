# The __init__.py file for the 'stores' subpackage within the CS-Cart API wrapper.

# This file is responsible for two primary functions:
# 1. It signals to Python that the directory containing it should be treated as a Python package.
#    This convention allows Python to understand the package structure and include these directories
#    in its package management system.

# 2. It imports and exposes specific classes, functions, or variables from the module within the
#    'stores' package. By doing so, it simplifies the import path required in other parts of the
#    application to access these components. In this case, everything (*) from the 'get_stores' module
#    is imported and made accessible directly via 'stores' package.

# Specifically, this setup is designed to streamline the use of the StoresService class, which
# encapsulates the functionality for interacting with the Stores API of the CS-Cart. After this import,
# other modules can directly use 'from stores import StoresService' without needing to specify the
# exact module within the 'stores' package where StoresService is defined.

from .get_stores import *
