


# this file is not name-specific as our __init__.py file is.

from setuptools import setup, find_packages

VERSION = '0.0.5' 
DESCRIPTION = 'tools to work with opencv on vscode'
LONG_DESCRIPTION = 'tools to work with opencv on vscode, like drawing and making images being printed'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="opencv_auxiliary_for_vscode", 
        version=VERSION,
        author="tms1991",
        author_email="<youremail@email.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=["numpy", "opencv-python", "matplotlib"], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['opencv', 'vscode'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)


# With that done, all we have to do next is run the following command in the same directory as base-verysimplemodule:

# python setup.py sdist bdist_wheel