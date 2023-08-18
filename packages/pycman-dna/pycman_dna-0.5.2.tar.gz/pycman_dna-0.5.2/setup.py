from setuptools import setup, find_packages

VERSION = '0.5.2' 
DESCRIPTION = 'Python Pacman Tool'
LONG_DESCRIPTION = 'A teaching tool based on arcade icon Pacman, written in Python. Requires Python 3.10 or above.'

# Setting up
setup(
       # the name must match the folder name
        name="pycman_dna", 
        version=VERSION,
        author="Liam Burns",
        author_email="l.burns@dundeeandangus.ac.uk",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['pygame'], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        include_package_data=True,
        package_data={'': ['maps/*', 'images/*', 'map_names.txt']},
        
        keywords=['python', 'pacman'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)