from setuptools import setup, find_packages

VERSION = '0.2.1' 
DESCRIPTION = 'PyGame Abstraction Library'
LONG_DESCRIPTION = 'A library of code which presents users with a simple, extensible program structure to make simple, 2D games with. Requires Python 3.10 or above.'

# Setting up
setup(
       # the name must match the folder name
        name="dna_engine", 
        version=VERSION,
        author="Liam Burns",
        author_email="l.burns@dundeeandangus.ac.uk",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['pygame', 'pyinstaller'], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'       
        
        keywords=['python', 'pygame', 'game development', 'beginner', 'education'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)